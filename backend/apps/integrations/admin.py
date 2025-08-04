"""
集成管理后台配置
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ShihuatongIntegration, ShihuatongMessage, ShihuatongUserMapping, IntegrationLog
)


@admin.register(ShihuatongIntegration)
class ShihuatongIntegrationAdmin(admin.ModelAdmin):
    """石化通集成管理"""
    list_display = [
        'name', 'status', 'success_rate_display', 'total_messages_sent', 
        'success_messages_sent', 'failed_messages_sent', 'last_used_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'status')
        }),
        ('配置信息', {
            'fields': ('webhook_url', 'app_code', 'app_key', 'app_secret', 'aes_key', 'aes_iv')
        }),
        ('统计信息', {
            'fields': ('total_messages_sent', 'success_messages_sent', 'failed_messages_sent')
        }),
    )
    
    readonly_fields = ['total_messages_sent', 'success_messages_sent', 'failed_messages_sent']
    
    def success_rate_display(self, obj):
        """成功率显示"""
        rate = obj.success_rate
        if rate >= 90:
            color = 'green'
        elif rate >= 70:
            color = 'orange'
        else:
            color = 'red'
        return format_html(f'<span style="color: {color};">{rate}%</span>')
    success_rate_display.short_description = '成功率'


@admin.register(ShihuatongMessage)
class ShihuatongMessageAdmin(admin.ModelAdmin):
    """石化通消息管理"""
    list_display = [
        'title', 'message_type', 'integration', 'status', 
        'retry_count', 'created_at', 'sent_at'
    ]
    list_filter = ['message_type', 'status', 'integration', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('integration', 'message_type', 'title', 'content')
        }),
        ('接收者信息', {
            'fields': ('hook_token', 'recipient_user_ids', 'mention_all')
        }),
        ('关联信息', {
            'fields': ('related_task', 'related_notification')
        }),
        ('发送状态', {
            'fields': ('status', 'response_data', 'error_message', 'retry_count')
        }),
    )
    
    readonly_fields = ['response_data', 'error_message', 'retry_count', 'sent_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('integration')


@admin.register(ShihuatongUserMapping)
class ShihuatongUserMappingAdmin(admin.ModelAdmin):
    """石化通用户映射管理"""
    list_display = [
        'user', 'shihuatong_username', 'shihuatong_display_name', 
        'status', 'verified_at', 'created_at'
    ]
    list_filter = ['status', 'verified_at', 'created_at']
    search_fields = ['user__real_name', 'shihuatong_username', 'shihuatong_display_name']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(IntegrationLog)
class IntegrationLogAdmin(admin.ModelAdmin):
    """集成日志管理"""
    list_display = [
        'integration', 'level', 'operation_type', 'message_preview', 
        'execution_time', 'created_at'
    ]
    list_filter = ['level', 'operation_type', 'created_at']
    search_fields = ['message']
    ordering = ['-created_at']
    readonly_fields = ['integration', 'level', 'operation_type', 'message', 'request_data', 'response_data']
    
    def message_preview(self, obj):
        """消息预览"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = '消息预览'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('integration')
