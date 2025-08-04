"""
任务相关信号处理器
自动发送通知和石化通消息
"""
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Task, TaskAssignment, TaskExecution, TaskReview
from apps.notifications.services import NotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=TaskAssignment)
def handle_task_assignment_created(sender, instance, created, **kwargs):
    """
    处理任务分配创建事件
    """
    if created:
        try:
            # 发送任务分配通知
            NotificationService.send_task_notification(
                task_id=str(instance.task.id),
                notification_type='task_assigned',
                recipient_ids=[instance.assignee.id],
                sender_id=instance.task.creator.id,
                extra_context={
                    'assignee_name': instance.assignee.real_name,
                    'assignment_role': instance.get_role_display(),
                    'is_primary': instance.is_primary
                }
            )
            
            logger.info(f"任务分配通知已发送: {instance.task.title} -> {instance.assignee.real_name}")
            
        except Exception as e:
            logger.error(f"发送任务分配通知失败: {e}", exc_info=True)


@receiver(post_save, sender=TaskAssignment)
def handle_task_assignment_status_changed(sender, instance, created, **kwargs):
    """
    处理任务分配状态变更事件
    """
    if not created:
        try:
            # 检查状态是否变为已完成
            if instance.status == TaskAssignment.AssignmentStatus.COMPLETED:
                # 检查任务是否所有分配都已完成
                all_completed = not instance.task.assignments.exclude(
                    status=TaskAssignment.AssignmentStatus.COMPLETED
                ).exists()
                
                if all_completed:
                    # 更新任务状态为已完成
                    instance.task.status = Task.TaskStatus.COMPLETED
                    instance.task.completed_at = timezone.now()
                    instance.task.save(update_fields=['status', 'completed_at'])
                    
                    # 发送任务完成通知给创建者
                    NotificationService.send_task_notification(
                        task_id=str(instance.task.id),
                        notification_type='task_completed',
                        recipient_ids=[instance.task.creator.id],
                        sender_id=instance.assignee.id,
                        extra_context={
                            'completed_by': instance.assignee.real_name,
                            'completed_at': instance.completed_at
                        }
                    )
                    
                    logger.info(f"任务完成通知已发送: {instance.task.title}")
            
            # 检查状态是否变为已拒绝
            elif instance.status == TaskAssignment.AssignmentStatus.REJECTED:
                # 发送任务拒绝通知给创建者
                NotificationService.create_notification(
                    recipient_id=instance.task.creator.id,
                    notification_type='task_updated',
                    title=f"任务被拒绝：{instance.task.title}",
                    content=f"{instance.assignee.real_name} 拒绝了任务：{instance.task.title}",
                    sender_id=instance.assignee.id,
                    related_task_id=str(instance.task.id),
                    channels=['system', 'shihuatong']
                )
                
                logger.info(f"任务拒绝通知已发送: {instance.task.title}")
                
        except Exception as e:
            logger.error(f"处理任务分配状态变更失败: {e}", exc_info=True)


@receiver(post_save, sender=TaskExecution)
def handle_task_execution_updated(sender, instance, created, **kwargs):
    """
    处理任务执行更新事件
    """
    try:
        # 如果进度有显著变化，发送进度更新通知
        if not created and instance.progress_percentage > 0:
            # 只在特定进度节点发送通知（25%, 50%, 75%）
            milestones = [25, 50, 75]
            if instance.progress_percentage in milestones:
                NotificationService.create_notification(
                    recipient_id=instance.assignment.task.creator.id,
                    notification_type='task_updated',
                    title=f"任务进度更新：{instance.assignment.task.title}",
                    content=f"{instance.assignment.assignee.real_name} 更新了任务进度：{instance.progress_percentage}%",
                    sender_id=instance.assignment.assignee.id,
                    related_task_id=str(instance.assignment.task.id),
                    channels=['system']
                )
                
                logger.info(f"任务进度通知已发送: {instance.assignment.task.title} - {instance.progress_percentage}%")
        
    except Exception as e:
        logger.error(f"处理任务执行更新失败: {e}", exc_info=True)


@receiver(post_save, sender=TaskReview)
def handle_task_review_created(sender, instance, created, **kwargs):
    """
    处理任务评价创建事件
    """
    if created:
        try:
            # 更新任务状态为已评价
            instance.task.status = Task.TaskStatus.REVIEWED
            instance.task.save(update_fields=['status'])
            
            # 获取所有执行人
            assignee_ids = list(instance.task.assignments.values_list('assignee_id', flat=True))
            
            # 发送评价通知给所有执行人
            NotificationService.send_task_notification(
                task_id=str(instance.task.id),
                notification_type='task_reviewed',
                recipient_ids=assignee_ids,
                sender_id=instance.reviewer.id,
                extra_context={
                    'reviewer_name': instance.reviewer.real_name,
                    'rating': instance.rating,
                    'overall_rating': instance.overall_rating,
                    'comments': instance.comments,
                    'is_satisfied': instance.is_satisfied
                }
            )
            
            logger.info(f"任务评价通知已发送: {instance.task.title}")
            
        except Exception as e:
            logger.error(f"发送任务评价通知失败: {e}", exc_info=True)


@receiver(pre_save, sender=Task)
def handle_task_status_change(sender, instance, **kwargs):
    """
    处理任务状态变更事件
    """
    try:
        if instance.pk:  # 只处理更新，不处理创建
            old_instance = Task.objects.get(pk=instance.pk)
            
            # 检查是否逾期
            if (instance.status != Task.TaskStatus.OVERDUE and 
                old_instance.status != Task.TaskStatus.OVERDUE and
                instance.is_overdue):
                
                instance.status = Task.TaskStatus.OVERDUE
                
                # 发送逾期通知
                assignee_ids = list(instance.assignments.values_list('assignee_id', flat=True))
                if assignee_ids:
                    NotificationService.send_task_notification(
                        task_id=str(instance.id),
                        notification_type='task_overdue',
                        recipient_ids=assignee_ids + [instance.creator.id],
                        extra_context={
                            'overdue_duration': timezone.now() - instance.due_date
                        }
                    )
                    
                    logger.info(f"任务逾期通知已发送: {instance.title}")
            
    except Task.DoesNotExist:
        pass  # 新创建的任务
    except Exception as e:
        logger.error(f"处理任务状态变更失败: {e}", exc_info=True)


@receiver(post_save, sender=Task)
def handle_task_published(sender, instance, created, **kwargs):
    """
    处理任务发布事件
    """
    if not created:
        try:
            # 检查任务是否从草稿状态变为待接收状态
            if instance.status == Task.TaskStatus.PENDING and not instance.published_at:
                instance.published_at = timezone.now()
                instance.save(update_fields=['published_at'])
                
                logger.info(f"任务已发布: {instance.title}")
                
        except Exception as e:
            logger.error(f"处理任务发布失败: {e}", exc_info=True)
