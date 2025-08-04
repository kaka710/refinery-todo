"""
部门管理后台配置
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Department, Profession, DepartmentCollaboration


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """部门管理"""
    list_display = [
        'name', 'code', 'type', 'parent', 'level',
        'status', 'users_count', 'created_at'
    ]
    list_filter = ['type', 'status', 'level', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['level', 'sort_order', 'name']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code', 'description', 'type')
        }),
        ('层级关系', {
            'fields': ('parent', 'sort_order')
        }),
        ('管理信息', {
            'fields': ('status',)
        }),
        ('联系信息', {
            'fields': ('phone', 'email', 'address')
        }),
    )
    
    readonly_fields = ['level']
    
    def users_count(self, obj):
        """用户数量"""
        return obj.users.filter(status='active').count()
    users_count.short_description = '用户数量'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """专业管理"""
    list_display = ['name', 'code', 'department', 'status', 'created_at']
    list_filter = ['department', 'status', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['department', 'sort_order', 'name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department')


@admin.register(DepartmentCollaboration)
class DepartmentCollaborationAdmin(admin.ModelAdmin):
    """部门协作关系管理"""
    list_display = [
        'primary_department', 'secondary_department', 
        'collaboration_type', 'is_active', 'created_at'
    ]
    list_filter = ['collaboration_type', 'is_active', 'created_at']
    search_fields = ['primary_department__name', 'secondary_department__name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'primary_department', 'secondary_department'
        )
