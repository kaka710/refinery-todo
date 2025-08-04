"""
通知相关信号处理器
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notification)
def handle_notification_created(sender, instance, created, **kwargs):
    """
    处理通知创建事件
    """
    if created:
        try:
            logger.info(f"新通知已创建: {instance.title} -> {instance.recipient.real_name}")
            
        except Exception as e:
            logger.error(f"处理通知创建事件失败: {e}", exc_info=True)
