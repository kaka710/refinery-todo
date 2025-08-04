"""
通知模型
支持多种通知方式：系统内通知、邮件、短信、石化通推送
"""
from django.db import models
import uuid


class Notification(models.Model):
    """
    通知主表
    """
    class NotificationType(models.TextChoices):
        TASK_ASSIGNED = 'task_assigned', '任务分配'
        TASK_UPDATED = 'task_updated', '任务更新'
        TASK_COMPLETED = 'task_completed', '任务完成'
        TASK_OVERDUE = 'task_overdue', '任务逾期'
        TASK_REVIEWED = 'task_reviewed', '任务评价'
        TASK_COMMENTED = 'task_commented', '任务评论'
        SYSTEM_ANNOUNCEMENT = 'system_announcement', '系统公告'
        USER_MENTIONED = 'user_mentioned', '用户提及'
    
    class NotificationStatus(models.TextChoices):
        UNREAD = 'unread', '未读'
        READ = 'read', '已读'
        ARCHIVED = 'archived', '已归档'
    
    class NotificationChannel(models.TextChoices):
        SYSTEM = 'system', '系统内通知'
        EMAIL = 'email', '邮件'
        SMS = 'sms', '短信'
        SHIHUATONG = 'shihuatong', '石化通'
    
    # 基本信息
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        verbose_name='通知类型'
    )
    
    # 发送者和接收者
    sender = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True,
        verbose_name='发送者'
    )
    recipient = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='received_notifications',
        verbose_name='接收者'
    )
    
    # 关联对象
    related_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='关联任务'
    )
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.UNREAD,
        verbose_name='通知状态'
    )
    
    # 发送渠道
    channels = models.JSONField(
        default=list,
        verbose_name='发送渠道',
        help_text='支持的渠道：system, email, sms, shihuatong'
    )
    
    # 额外数据
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='额外数据'
    )
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['notification_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} -> {self.recipient.real_name}"
    
    def mark_as_read(self):
        """标记为已读"""
        from django.utils import timezone
        if self.status == self.NotificationStatus.UNREAD:
            self.status = self.NotificationStatus.READ
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])


class NotificationTemplate(models.Model):
    """
    通知模板
    用于标准化通知内容
    """
    class TemplateStatus(models.TextChoices):
        ACTIVE = 'active', '启用'
        INACTIVE = 'inactive', '停用'
    
    # 基本信息
    name = models.CharField(max_length=100, verbose_name='模板名称')
    notification_type = models.CharField(
        max_length=30,
        choices=Notification.NotificationType.choices,
        verbose_name='通知类型'
    )
    
    # 模板内容
    title_template = models.CharField(max_length=200, verbose_name='标题模板')
    content_template = models.TextField(verbose_name='内容模板')
    
    # 默认渠道
    default_channels = models.JSONField(
        default=list,
        verbose_name='默认发送渠道'
    )
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=TemplateStatus.choices,
        default=TemplateStatus.ACTIVE,
        verbose_name='模板状态'
    )
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'notification_templates'
        verbose_name = '通知模板'
        verbose_name_plural = '通知模板'
        unique_together = [['notification_type', 'name']]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.name}"
    
    def render(self, context):
        """渲染模板"""
        from django.template import Template, Context
        
        title_template = Template(self.title_template)
        content_template = Template(self.content_template)
        
        django_context = Context(context)
        
        return {
            'title': title_template.render(django_context),
            'content': content_template.render(django_context),
            'channels': self.default_channels
        }


class NotificationLog(models.Model):
    """
    通知发送日志
    记录通知的发送状态和结果
    """
    class SendStatus(models.TextChoices):
        PENDING = 'pending', '待发送'
        SENDING = 'sending', '发送中'
        SUCCESS = 'success', '发送成功'
        FAILED = 'failed', '发送失败'
        RETRY = 'retry', '重试中'
    
    # 关联通知
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='send_logs',
        verbose_name='通知'
    )
    
    # 发送信息
    channel = models.CharField(
        max_length=20,
        choices=Notification.NotificationChannel.choices,
        verbose_name='发送渠道'
    )
    status = models.CharField(
        max_length=20,
        choices=SendStatus.choices,
        default=SendStatus.PENDING,
        verbose_name='发送状态'
    )
    
    # 发送结果
    response_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='响应数据'
    )
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    
    # 重试信息
    retry_count = models.PositiveIntegerField(default=0, verbose_name='重试次数')
    max_retries = models.PositiveIntegerField(default=3, verbose_name='最大重试次数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='发送时间')
    
    class Meta:
        db_table = 'notification_logs'
        verbose_name = '通知发送日志'
        verbose_name_plural = '通知发送日志'
        ordering = ['-created_at']
        unique_together = [['notification', 'channel']]
    
    def __str__(self):
        return f"{self.notification.title} - {self.get_channel_display()} - {self.get_status_display()}"
    
    @property
    def can_retry(self):
        """是否可以重试"""
        return (
            self.status == self.SendStatus.FAILED and 
            self.retry_count < self.max_retries
        )


class UserNotificationSettings(models.Model):
    """
    用户通知设置
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notification_settings',
        verbose_name='用户'
    )
    
    # 通知渠道开关
    system_notifications = models.BooleanField(default=True, verbose_name='系统内通知')
    email_notifications = models.BooleanField(default=True, verbose_name='邮件通知')
    sms_notifications = models.BooleanField(default=False, verbose_name='短信通知')
    shihuatong_notifications = models.BooleanField(default=True, verbose_name='石化通通知')
    
    # 通知类型开关
    task_assigned_notifications = models.BooleanField(default=True, verbose_name='任务分配通知')
    task_updated_notifications = models.BooleanField(default=True, verbose_name='任务更新通知')
    task_completed_notifications = models.BooleanField(default=True, verbose_name='任务完成通知')
    task_overdue_notifications = models.BooleanField(default=True, verbose_name='任务逾期通知')
    task_reviewed_notifications = models.BooleanField(default=True, verbose_name='任务评价通知')
    task_commented_notifications = models.BooleanField(default=True, verbose_name='任务评论通知')
    
    # 免打扰时间
    do_not_disturb_start = models.TimeField(null=True, blank=True, verbose_name='免打扰开始时间')
    do_not_disturb_end = models.TimeField(null=True, blank=True, verbose_name='免打扰结束时间')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_notification_settings'
        verbose_name = '用户通知设置'
        verbose_name_plural = '用户通知设置'
    
    def __str__(self):
        return f"{self.user.real_name}的通知设置"
    
    def is_channel_enabled(self, channel):
        """检查指定渠道是否启用"""
        channel_mapping = {
            'system': self.system_notifications,
            'email': self.email_notifications,
            'sms': self.sms_notifications,
            'shihuatong': self.shihuatong_notifications,
        }
        return channel_mapping.get(channel, False)
    
    def is_notification_type_enabled(self, notification_type):
        """检查指定通知类型是否启用"""
        type_mapping = {
            'task_assigned': self.task_assigned_notifications,
            'task_updated': self.task_updated_notifications,
            'task_completed': self.task_completed_notifications,
            'task_overdue': self.task_overdue_notifications,
            'task_reviewed': self.task_reviewed_notifications,
            'task_commented': self.task_commented_notifications,
        }
        return type_mapping.get(notification_type, True)
