"""
用户管理后台配置
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, UserProfile, UserLoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = [
        'username', 'employee_id', 'real_name', 'email', 'role', 
        'department', 'status', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'status', 'is_active', 'department', 'date_joined']
    search_fields = ['username', 'employee_id', 'real_name', 'email']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {
            'fields': ('employee_id', 'real_name', 'email', 'phone')
        }),
        ('权限信息', {
            'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('组织信息', {
            'fields': ('department', 'shihuatong_user_id')
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined', 'last_login_ip')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'employee_id', 'real_name', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login', 'last_login_ip']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理"""
    list_display = ['user', 'position', 'office_location', 'email_notifications', 'sms_notifications']
    list_filter = ['email_notifications', 'sms_notifications', 'shihuatong_notifications']
    search_fields = ['user__real_name', 'position']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    """登录日志管理"""
    list_display = ['user', 'ip_address', 'login_time', 'is_success', 'failure_reason']
    list_filter = ['is_success', 'login_time']
    search_fields = ['user__real_name', 'ip_address']
    ordering = ['-login_time']
    readonly_fields = ['user', 'ip_address', 'user_agent', 'login_time', 'is_success', 'failure_reason']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
