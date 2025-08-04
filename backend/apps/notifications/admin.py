"""
通知管理后台配置
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Notification, NotificationTemplate, NotificationLog, UserNotificationSettings
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """通知管理"""
    list_display = [
        'title', 'notification_type', 'sender', 'recipient', 
        'status', 'channels_display', 'created_at'
    ]
    list_filter = ['notification_type', 'status', 'created_at']
    search_fields = ['title', 'content', 'recipient__real_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'notification_type')
        }),
        ('发送信息', {
            'fields': ('sender', 'recipient', 'channels')
        }),
        ('关联信息', {
            'fields': ('related_task', 'extra_data')
        }),
        ('状态信息', {
            'fields': ('status', 'read_at')
        }),
    )
    
    readonly_fields = ['read_at']
    
    def channels_display(self, obj):
        """渠道显示"""
        if obj.channels:
            return ', '.join(obj.channels)
        return '-'
    channels_display.short_description = '发送渠道'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'recipient')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """通知模板管理"""
    list_display = ['name', 'notification_type', 'status', 'created_at']
    list_filter = ['notification_type', 'status', 'created_at']
    search_fields = ['name', 'title_template', 'content_template']
    ordering = ['-created_at']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """通知发送日志管理"""
    list_display = [
        'notification', 'channel', 'status', 'retry_count', 
        'created_at', 'sent_at'
    ]
    list_filter = ['channel', 'status', 'created_at']
    search_fields = ['notification__title']
    ordering = ['-created_at']
    readonly_fields = ['notification', 'channel', 'status', 'response_data', 'error_message']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserNotificationSettings)
class UserNotificationSettingsAdmin(admin.ModelAdmin):
    """用户通知设置管理"""
    list_display = [
        'user', 'system_notifications', 'email_notifications', 
        'sms_notifications', 'shihuatong_notifications'
    ]
    list_filter = [
        'system_notifications', 'email_notifications', 
        'sms_notifications', 'shihuatong_notifications'
    ]
    search_fields = ['user__real_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
