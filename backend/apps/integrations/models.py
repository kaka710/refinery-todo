"""
第三方集成模型
主要用于石化通系统集成
"""
from django.db import models
import uuid


class ShihuatongIntegration(models.Model):
    """
    石化通集成配置
    """
    class IntegrationStatus(models.TextChoices):
        ACTIVE = 'active', '启用'
        INACTIVE = 'inactive', '停用'
        ERROR = 'error', '错误'
    
    # 基本信息
    name = models.CharField(max_length=100, verbose_name='集成名称')
    description = models.TextField(blank=True, verbose_name='描述')
    
    # 配置信息
    webhook_url = models.URLField(verbose_name='Webhook URL')
    app_code = models.CharField(max_length=100, verbose_name='应用编码')
    app_key = models.CharField(max_length=100, verbose_name='应用Key')
    app_secret = models.CharField(max_length=200, verbose_name='应用Secret')
    aes_key = models.CharField(max_length=100, verbose_name='AES密钥')
    aes_iv = models.CharField(max_length=100, verbose_name='AES初始向量')
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=IntegrationStatus.choices,
        default=IntegrationStatus.ACTIVE,
        verbose_name='集成状态'
    )
    
    # 统计信息
    total_messages_sent = models.PositiveIntegerField(default=0, verbose_name='总发送消息数')
    success_messages_sent = models.PositiveIntegerField(default=0, verbose_name='成功发送消息数')
    failed_messages_sent = models.PositiveIntegerField(default=0, verbose_name='失败发送消息数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name='最后使用时间')
    
    class Meta:
        db_table = 'shihuatong_integrations'
        verbose_name = '石化通集成'
        verbose_name_plural = '石化通集成'
    
    def __str__(self):
        return self.name
    
    @property
    def success_rate(self):
        """成功率"""
        if self.total_messages_sent == 0:
            return 0
        return round((self.success_messages_sent / self.total_messages_sent) * 100, 2)


class ShihuatongMessage(models.Model):
    """
    石化通消息记录
    """
    class MessageType(models.TextChoices):
        TEXT = 'text', '文本消息'
        MARKDOWN = 'markdown', 'Markdown消息'
        CARD = 'card', '卡片消息'
    
    class MessageStatus(models.TextChoices):
        PENDING = 'pending', '待发送'
        SENDING = 'sending', '发送中'
        SUCCESS = 'success', '发送成功'
        FAILED = 'failed', '发送失败'
        RETRY = 'retry', '重试中'
    
    # 基本信息
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integration = models.ForeignKey(
        ShihuatongIntegration,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='集成配置'
    )
    
    # 消息内容
    message_type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT,
        verbose_name='消息类型'
    )
    title = models.CharField(max_length=200, verbose_name='消息标题')
    content = models.TextField(verbose_name='消息内容')
    
    # 接收者信息
    hook_token = models.CharField(max_length=200, verbose_name='Hook Token')
    recipient_user_ids = models.JSONField(
        default=list,
        blank=True,
        verbose_name='接收用户ID列表'
    )
    mention_all = models.BooleanField(default=False, verbose_name='是否@所有人')
    
    # 关联信息
    related_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shihuatong_messages',
        verbose_name='关联任务'
    )
    related_notification = models.ForeignKey(
        'notifications.Notification',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shihuatong_messages',
        verbose_name='关联通知'
    )
    
    # 发送状态
    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.PENDING,
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
        db_table = 'shihuatong_messages'
        verbose_name = '石化通消息'
        verbose_name_plural = '石化通消息'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['related_task']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    @property
    def can_retry(self):
        """是否可以重试"""
        return (
            self.status == self.MessageStatus.FAILED and 
            self.retry_count < self.max_retries
        )


class ShihuatongUserMapping(models.Model):
    """
    石化通用户映射
    将系统用户与石化通用户关联
    """
    class MappingStatus(models.TextChoices):
        ACTIVE = 'active', '正常'
        INACTIVE = 'inactive', '停用'
        PENDING = 'pending', '待验证'
    
    # 系统用户
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='shihuatong_mapping',
        verbose_name='系统用户'
    )
    
    # 石化通用户信息
    shihuatong_user_id = models.CharField(max_length=100, verbose_name='石化通用户ID')
    shihuatong_username = models.CharField(max_length=100, verbose_name='石化通用户名')
    shihuatong_display_name = models.CharField(max_length=100, verbose_name='石化通显示名称')
    
    # 群组信息
    default_hook_token = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='默认Hook Token'
    )
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=MappingStatus.choices,
        default=MappingStatus.PENDING,
        verbose_name='映射状态'
    )
    
    # 验证信息
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='验证时间')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'shihuatong_user_mappings'
        verbose_name = '石化通用户映射'
        verbose_name_plural = '石化通用户映射'
        unique_together = [['shihuatong_user_id']]
    
    def __str__(self):
        return f"{self.user.real_name} -> {self.shihuatong_display_name}"


class IntegrationLog(models.Model):
    """
    集成操作日志
    """
    class LogLevel(models.TextChoices):
        DEBUG = 'debug', '调试'
        INFO = 'info', '信息'
        WARNING = 'warning', '警告'
        ERROR = 'error', '错误'
        CRITICAL = 'critical', '严重'
    
    class OperationType(models.TextChoices):
        SEND_MESSAGE = 'send_message', '发送消息'
        USER_SYNC = 'user_sync', '用户同步'
        CONFIG_UPDATE = 'config_update', '配置更新'
        HEALTH_CHECK = 'health_check', '健康检查'
    
    # 基本信息
    integration = models.ForeignKey(
        ShihuatongIntegration,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='集成配置'
    )
    
    # 日志信息
    level = models.CharField(
        max_length=20,
        choices=LogLevel.choices,
        verbose_name='日志级别'
    )
    operation_type = models.CharField(
        max_length=30,
        choices=OperationType.choices,
        verbose_name='操作类型'
    )
    message = models.TextField(verbose_name='日志消息')
    
    # 详细信息
    request_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='请求数据'
    )
    response_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='响应数据'
    )
    
    # 执行信息
    execution_time = models.FloatField(null=True, blank=True, verbose_name='执行时间(秒)')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'integration_logs'
        verbose_name = '集成日志'
        verbose_name_plural = '集成日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['operation_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.integration.name} - {self.get_level_display()} - {self.message[:50]}"
