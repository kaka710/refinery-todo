"""
通知服务
统一管理各种通知渠道的发送
"""
import logging
from typing import List, Dict, Any, Optional
from django.utils import timezone

from .models import (
    Notification, 
    NotificationTemplate, 
    NotificationLog, 
    UserNotificationSettings
)
from apps.integrations.tasks import send_shihuatong_message_task

logger = logging.getLogger(__name__)


class NotificationService:
    """
    通知服务类
    """
    
    @staticmethod
    def create_notification(
        recipient_id: int,
        notification_type: str,
        title: str,
        content: str,
        sender_id: Optional[int] = None,
        related_task_id: Optional[str] = None,
        channels: Optional[List[str]] = None,
        extra_data: Optional[Dict] = None
    ) -> Notification:
        """
        创建通知
        
        Args:
            recipient_id: 接收者ID
            notification_type: 通知类型
            title: 通知标题
            content: 通知内容
            sender_id: 发送者ID
            related_task_id: 关联任务ID
            channels: 发送渠道列表
            extra_data: 额外数据
            
        Returns:
            Notification实例
        """
        from apps.users.models import User
        
        try:
            recipient = User.objects.get(id=recipient_id)
            sender = User.objects.get(id=sender_id) if sender_id else None
            
            # 获取用户通知设置
            settings = NotificationService._get_user_notification_settings(recipient)
            
            # 根据用户设置过滤渠道
            if channels is None:
                channels = ['system']  # 默认系统内通知
            
            filtered_channels = NotificationService._filter_channels_by_user_settings(
                channels, notification_type, settings
            )
            
            # 创建通知
            notification = Notification.objects.create(
                title=title,
                content=content,
                notification_type=notification_type,
                sender=sender,
                recipient=recipient,
                related_task_id=related_task_id,
                channels=filtered_channels,
                extra_data=extra_data or {}
            )
            
            # 异步发送通知
            NotificationService._send_notification_async(notification)
            
            return notification
            
        except Exception as e:
            logger.error(f"创建通知失败: {e}", exc_info=True)
            raise e
    
    @staticmethod
    def create_notification_from_template(
        template_name: str,
        notification_type: str,
        recipient_id: int,
        context: Dict[str, Any],
        sender_id: Optional[int] = None,
        related_task_id: Optional[str] = None
    ) -> Notification:
        """
        从模板创建通知
        
        Args:
            template_name: 模板名称
            notification_type: 通知类型
            recipient_id: 接收者ID
            context: 模板上下文
            sender_id: 发送者ID
            related_task_id: 关联任务ID
            
        Returns:
            Notification实例
        """
        try:
            template = NotificationTemplate.objects.get(
                name=template_name,
                notification_type=notification_type,
                status=NotificationTemplate.TemplateStatus.ACTIVE
            )
            
            # 渲染模板
            rendered = template.render(context)
            
            return NotificationService.create_notification(
                recipient_id=recipient_id,
                notification_type=notification_type,
                title=rendered['title'],
                content=rendered['content'],
                sender_id=sender_id,
                related_task_id=related_task_id,
                channels=rendered['channels']
            )
            
        except NotificationTemplate.DoesNotExist:
            logger.error(f"通知模板不存在: {template_name} - {notification_type}")
            raise ValueError(f"通知模板不存在: {template_name}")
        except Exception as e:
            logger.error(f"从模板创建通知失败: {e}", exc_info=True)
            raise e
    
    @staticmethod
    def send_task_notification(
        task_id: str,
        notification_type: str,
        recipient_ids: List[int],
        sender_id: Optional[int] = None,
        extra_context: Optional[Dict] = None
    ):
        """
        发送任务相关通知
        
        Args:
            task_id: 任务ID
            notification_type: 通知类型
            recipient_ids: 接收者ID列表
            sender_id: 发送者ID
            extra_context: 额外上下文
        """
        try:
            from apps.tasks.models import Task
            
            task = Task.objects.get(id=task_id)
            
            # 构建上下文
            context = {
                'task': task,
                'task_title': task.title,
                'task_description': task.description,
                'creator_name': task.creator.real_name,
                'due_date': task.due_date,
                'start_date': task.start_date,
                **(extra_context or {})
            }
            
            # 为每个接收者创建通知
            for recipient_id in recipient_ids:
                try:
                    NotificationService.create_notification_from_template(
                        template_name='default',
                        notification_type=notification_type,
                        recipient_id=recipient_id,
                        context=context,
                        sender_id=sender_id,
                        related_task_id=task_id
                    )
                except Exception as e:
                    logger.error(f"为用户 {recipient_id} 创建任务通知失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"发送任务通知失败: {e}", exc_info=True)
    
    @staticmethod
    def _get_user_notification_settings(user) -> UserNotificationSettings:
        """获取用户通知设置"""
        settings, created = UserNotificationSettings.objects.get_or_create(
            user=user,
            defaults={
                'system_notifications': True,
                'email_notifications': True,
                'sms_notifications': False,
                'shihuatong_notifications': True,
            }
        )
        return settings
    
    @staticmethod
    def _filter_channels_by_user_settings(
        channels: List[str], 
        notification_type: str, 
        settings: UserNotificationSettings
    ) -> List[str]:
        """根据用户设置过滤通知渠道"""
        filtered_channels = []
        
        for channel in channels:
            # 检查渠道是否启用
            if not settings.is_channel_enabled(channel):
                continue
                
            # 检查通知类型是否启用
            if not settings.is_notification_type_enabled(notification_type):
                continue
                
            # 检查免打扰时间
            if NotificationService._is_do_not_disturb_time(settings):
                if channel in ['sms', 'shihuatong']:  # 免打扰时间不发送短信和石化通
                    continue
            
            filtered_channels.append(channel)
        
        # 至少保留系统内通知
        if not filtered_channels and 'system' in channels:
            filtered_channels = ['system']
        
        return filtered_channels
    
    @staticmethod
    def _is_do_not_disturb_time(settings: UserNotificationSettings) -> bool:
        """检查是否在免打扰时间内"""
        if not settings.do_not_disturb_start or not settings.do_not_disturb_end:
            return False
        
        current_time = timezone.now().time()
        start_time = settings.do_not_disturb_start
        end_time = settings.do_not_disturb_end
        
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:  # 跨天的情况
            return current_time >= start_time or current_time <= end_time
    
    @staticmethod
    def _send_notification_async(notification: Notification):
        """异步发送通知"""
        for channel in notification.channels:
            try:
                if channel == 'system':
                    # 系统内通知已经创建，无需额外处理
                    NotificationService._log_notification_send(
                        notification, channel, 'success'
                    )
                    
                elif channel == 'email':
                    # 发送邮件通知
                    NotificationService._send_email_notification(notification)
                    
                elif channel == 'sms':
                    # 发送短信通知
                    NotificationService._send_sms_notification(notification)
                    
                elif channel == 'shihuatong':
                    # 发送石化通通知
                    NotificationService._send_shihuatong_notification(notification)
                    
            except Exception as e:
                logger.error(f"发送通知失败 - 渠道: {channel}, 错误: {e}")
                NotificationService._log_notification_send(
                    notification, channel, 'failed', str(e)
                )
    
    @staticmethod
    def _send_email_notification(notification: Notification):
        """发送邮件通知"""
        # TODO: 实现邮件发送逻辑
        logger.info(f"发送邮件通知: {notification.title} -> {notification.recipient.email}")
        NotificationService._log_notification_send(notification, 'email', 'success')
    
    @staticmethod
    def _send_sms_notification(notification: Notification):
        """发送短信通知"""
        # TODO: 实现短信发送逻辑
        logger.info(f"发送短信通知: {notification.title} -> {notification.recipient.phone}")
        NotificationService._log_notification_send(notification, 'sms', 'success')
    
    @staticmethod
    def _send_shihuatong_notification(notification: Notification):
        """发送石化通通知"""
        try:
            from apps.integrations.models import ShihuatongUserMapping
            
            # 获取用户的石化通映射
            mapping = ShihuatongUserMapping.objects.get(
                user=notification.recipient,
                status=ShihuatongUserMapping.MappingStatus.ACTIVE
            )
            
            if mapping.default_hook_token:
                # 异步发送石化通消息
                send_shihuatong_message_task.delay(
                    hook_token=mapping.default_hook_token,
                    title=notification.title,
                    content=notification.content,
                    message_type='text',
                    mention_all=False,
                    user_ids=[mapping.shihuatong_user_id],
                    related_task_id=notification.related_task_id,
                    related_notification_id=str(notification.id)
                )
                
                NotificationService._log_notification_send(
                    notification, 'shihuatong', 'pending'
                )
            else:
                raise ValueError("用户没有配置默认Hook Token")
                
        except ShihuatongUserMapping.DoesNotExist:
            logger.warning(f"用户 {notification.recipient.real_name} 没有石化通映射配置")
            NotificationService._log_notification_send(
                notification, 'shihuatong', 'failed', '用户没有石化通映射配置'
            )
        except Exception as e:
            logger.error(f"发送石化通通知失败: {e}")
            NotificationService._log_notification_send(
                notification, 'shihuatong', 'failed', str(e)
            )
    
    @staticmethod
    def _log_notification_send(
        notification: Notification, 
        channel: str, 
        status: str, 
        error_message: str = ''
    ):
        """记录通知发送日志"""
        NotificationLog.objects.create(
            notification=notification,
            channel=channel,
            status=status,
            error_message=error_message,
            sent_at=timezone.now() if status == 'success' else None
        )
    
    @staticmethod
    def mark_notification_as_read(notification_id: str, user_id: int) -> bool:
        """标记通知为已读"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient_id=user_id
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @staticmethod
    def get_user_unread_count(user_id: int) -> int:
        """获取用户未读通知数量"""
        return Notification.objects.filter(
            recipient_id=user_id,
            status=Notification.NotificationStatus.UNREAD
        ).count()
    
    @staticmethod
    def get_user_notifications(
        user_id: int, 
        status: Optional[str] = None,
        notification_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Notification]:
        """获取用户通知列表"""
        queryset = Notification.objects.filter(recipient_id=user_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        return list(queryset.order_by('-created_at')[:limit])
