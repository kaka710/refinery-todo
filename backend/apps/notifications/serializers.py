"""
通知相关序列化器
"""
from rest_framework import serializers
from .models import (
    Notification, NotificationTemplate, NotificationLog, UserNotificationSettings
)
from apps.users.serializers import UserSimpleSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    sender = UserSimpleSerializer(read_only=True)
    recipient = UserSimpleSerializer(read_only=True)
    related_task_title = serializers.CharField(
        source='related_task.title', read_only=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'content', 'notification_type',
            'sender', 'recipient', 'related_task', 'related_task_title',
            'status', 'channels', 'extra_data',
            'created_at', 'read_at'
        ]
        read_only_fields = ['sender', 'recipient', 'created_at', 'read_at']


class NotificationSimpleSerializer(serializers.ModelSerializer):
    """通知简单序列化器"""
    sender_name = serializers.CharField(source='sender.real_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'notification_type', 'sender_name',
            'status', 'created_at'
        ]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """通知模板序列化器"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'notification_type', 'title_template',
            'content_template', 'default_channels', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class NotificationLogSerializer(serializers.ModelSerializer):
    """通知发送日志序列化器"""
    notification_title = serializers.CharField(
        source='notification.title', read_only=True
    )
    recipient_name = serializers.CharField(
        source='notification.recipient.real_name', read_only=True
    )
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'notification_title', 'recipient_name',
            'channel', 'status', 'response_data', 'error_message',
            'retry_count', 'max_retries', 'created_at', 'sent_at'
        ]
        read_only_fields = ['created_at', 'sent_at']


class UserNotificationSettingsSerializer(serializers.ModelSerializer):
    """用户通知设置序列化器"""
    
    class Meta:
        model = UserNotificationSettings
        fields = [
            'system_notifications', 'email_notifications', 
            'sms_notifications', 'shihuatong_notifications',
            'task_assigned_notifications', 'task_updated_notifications',
            'task_completed_notifications', 'task_overdue_notifications',
            'task_reviewed_notifications', 'task_commented_notifications',
            'do_not_disturb_start', 'do_not_disturb_end'
        ]


class NotificationCreateSerializer(serializers.Serializer):
    """创建通知序列化器"""
    recipient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='接收者ID列表'
    )
    notification_type = serializers.ChoiceField(
        choices=Notification.NotificationType.choices
    )
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=Notification.NotificationChannel.choices),
        required=False,
        default=['system']
    )
    related_task_id = serializers.UUIDField(required=False)
    extra_data = serializers.JSONField(required=False, default=dict)


class NotificationStatsSerializer(serializers.Serializer):
    """通知统计序列化器"""
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    notifications_by_type = serializers.DictField()
    notifications_by_channel = serializers.DictField()
    recent_notifications = NotificationSimpleSerializer(many=True)
