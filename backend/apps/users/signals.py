"""
用户相关信号处理器
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile
from apps.notifications.models import UserNotificationSettings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile_and_settings(sender, instance, created, **kwargs):
    """
    用户创建后自动创建用户资料和通知设置
    """
    if created:
        try:
            # 创建用户资料
            UserProfile.objects.create(user=instance)
            
            # 创建通知设置
            UserNotificationSettings.objects.create(
                user=instance,
                system_notifications=True,
                email_notifications=True,
                sms_notifications=False,
                shihuatong_notifications=True,
                task_assigned_notifications=True,
                task_updated_notifications=True,
                task_completed_notifications=True,
                task_overdue_notifications=True,
                task_reviewed_notifications=True,
                task_commented_notifications=True
            )
            
            logger.info(f"用户资料和通知设置已创建: {instance.real_name}")
            
        except Exception as e:
            logger.error(f"创建用户资料和设置失败: {e}", exc_info=True)
