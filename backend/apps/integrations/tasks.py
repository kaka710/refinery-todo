"""
石化通集成异步任务
"""
import logging
from typing import Dict, List, Optional
from celery import shared_task
from django.utils import timezone

from .services import ShihuatongService
from .models import ShihuatongMessage, ShihuatongUserMapping
from apps.notifications.models import Notification

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_shihuatong_message_task(
    self,
    hook_token: str,
    title: str,
    content: str,
    message_type: str = 'text',
    mention_all: bool = False,
    user_ids: Optional[List[str]] = None,
    related_task_id: Optional[str] = None,
    related_notification_id: Optional[str] = None,
    integration_id: Optional[int] = None
):
    """
    异步发送石化通消息任务
    
    Args:
        hook_token: Hook Token
        title: 消息标题
        content: 消息内容
        message_type: 消息类型
        mention_all: 是否@所有人
        user_ids: 指定用户ID列表
        related_task_id: 关联任务ID
        related_notification_id: 关联通知ID
        integration_id: 集成配置ID
    """
    try:
        service = ShihuatongService(integration_id)
        
        message = service.send_message(
            hook_token=hook_token,
            title=title,
            content=content,
            message_type=message_type,
            mention_all=mention_all,
            user_ids=user_ids,
            related_task_id=related_task_id,
            related_notification_id=related_notification_id
        )
        
        if message.status == ShihuatongMessage.MessageStatus.FAILED:
            # 如果发送失败，根据重试策略决定是否重试
            if self.request.retries < self.max_retries:
                logger.warning(f"石化通消息发送失败，准备重试: {message.error_message}")
                raise self.retry(countdown=60 * (self.request.retries + 1))
            else:
                logger.error(f"石化通消息发送最终失败: {message.error_message}")
        
        return {
            "message_id": str(message.id),
            "status": message.status,
            "title": title
        }
        
    except Exception as e:
        logger.error(f"发送石化通消息任务异常: {e}", exc_info=True)
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (self.request.retries + 1), exc=e)
        else:
            raise e


@shared_task
def send_task_notification_to_shihuatong(
    task_id: str,
    notification_type: str,
    recipient_user_ids: List[int]
):
    """
    发送任务相关通知到石化通
    
    Args:
        task_id: 任务ID
        notification_type: 通知类型
        recipient_user_ids: 接收用户ID列表
    """
    try:
        from apps.tasks.models import Task
        from apps.users.models import User
        
        # 获取任务信息
        task = Task.objects.get(id=task_id)
        
        # 获取接收用户
        recipients = User.objects.filter(id__in=recipient_user_ids)
        
        # 构建消息内容
        title, content = _build_task_notification_content(task, notification_type)
        
        # 为每个用户发送消息
        for user in recipients:
            try:
                # 获取用户的石化通映射
                mapping = ShihuatongUserMapping.objects.get(
                    user=user,
                    status=ShihuatongUserMapping.MappingStatus.ACTIVE
                )
                
                if mapping.default_hook_token:
                    # 发送消息
                    send_shihuatong_message_task.delay(
                        hook_token=mapping.default_hook_token,
                        title=title,
                        content=content,
                        message_type='text',
                        mention_all=False,
                        user_ids=[mapping.shihuatong_user_id],
                        related_task_id=task_id
                    )
                    
            except ShihuatongUserMapping.DoesNotExist:
                logger.warning(f"用户 {user.real_name} 没有石化通映射配置")
                continue
            except Exception as e:
                logger.error(f"为用户 {user.real_name} 发送石化通通知失败: {e}")
                continue
                
    except Exception as e:
        logger.error(f"发送任务通知到石化通失败: {e}", exc_info=True)


@shared_task
def retry_failed_messages():
    """
    重试失败的消息
    """
    try:
        # 获取可重试的失败消息
        failed_messages = ShihuatongMessage.objects.filter(
            status=ShihuatongMessage.MessageStatus.FAILED,
            retry_count__lt=3,
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        service = ShihuatongService()
        retry_count = 0
        
        for message in failed_messages:
            if service.retry_failed_message(str(message.id)):
                retry_count += 1
        
        logger.info(f"重试了 {retry_count} 条失败消息")
        
        return {
            "total_failed": failed_messages.count(),
            "retry_count": retry_count
        }
        
    except Exception as e:
        logger.error(f"重试失败消息任务异常: {e}", exc_info=True)
        raise e


@shared_task
def cleanup_old_messages():
    """
    清理旧消息记录
    """
    try:
        # 删除30天前的消息记录
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        
        deleted_count = ShihuatongMessage.objects.filter(
            created_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"清理了 {deleted_count} 条旧消息记录")
        
        return {"deleted_count": deleted_count}
        
    except Exception as e:
        logger.error(f"清理旧消息任务异常: {e}", exc_info=True)
        raise e


@shared_task
def sync_shihuatong_users():
    """
    同步石化通用户信息
    """
    try:
        # 这里可以实现与石化通系统的用户同步逻辑
        # 由于没有具体的用户同步API，这里只是一个占位符
        
        logger.info("石化通用户同步任务执行完成")
        
        return {"status": "completed"}
        
    except Exception as e:
        logger.error(f"同步石化通用户任务异常: {e}", exc_info=True)
        raise e


def _build_task_notification_content(task, notification_type: str) -> tuple:
    """
    构建任务通知内容
    
    Args:
        task: 任务对象
        notification_type: 通知类型
        
    Returns:
        (title, content) 元组
    """
    from apps.tasks.models import Task
    
    if notification_type == 'task_assigned':
        title = f"【任务分配】{task.title}"
        content = f"""
您有新的任务需要处理：

任务标题：{task.title}
任务类型：{task.get_task_type_display()}
优先级：{task.get_priority_display()}
创建者：{task.creator.real_name}
开始时间：{task.start_date.strftime('%Y-%m-%d %H:%M')}
截止时间：{task.due_date.strftime('%Y-%m-%d %H:%M')}

任务描述：
{task.description}

请及时处理！
        """.strip()
        
    elif notification_type == 'task_completed':
        title = f"【任务完成】{task.title}"
        content = f"""
任务已完成，请查看执行结果：

任务标题：{task.title}
完成时间：{task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else '刚刚'}
执行人：{', '.join([assignment.assignee.real_name for assignment in task.assignments.all()])}

请及时进行评价！
        """.strip()
        
    elif notification_type == 'task_overdue':
        title = f"【任务逾期】{task.title}"
        content = f"""
任务已逾期，请尽快处理：

任务标题：{task.title}
截止时间：{task.due_date.strftime('%Y-%m-%d %H:%M')}
逾期时长：{timezone.now() - task.due_date}

请立即处理！
        """.strip()
        
    elif notification_type == 'task_reviewed':
        title = f"【任务评价】{task.title}"
        content = f"""
您的任务已被评价：

任务标题：{task.title}
评价人：{task.review.reviewer.real_name if hasattr(task, 'review') else '未知'}
评价时间：{task.review.reviewed_at.strftime('%Y-%m-%d %H:%M') if hasattr(task, 'review') else '刚刚'}

请查看详细评价内容！
        """.strip()
        
    else:
        title = f"【任务通知】{task.title}"
        content = f"任务 {task.title} 有新的更新，请查看详情。"
    
    return title, content
