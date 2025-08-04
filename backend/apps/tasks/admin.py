"""
任务管理后台配置
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Task, TaskAssignment, TaskExecution, TaskReview, 
    TaskAttachment, TaskComment, TaskTemplate
)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """任务管理"""
    list_display = [
        'title', 'task_type', 'priority', 'status', 'creator', 
        'creator_department', 'due_date', 'is_overdue', 'created_at'
    ]
    list_filter = [
        'task_type', 'priority', 'status', 'creator_department', 
        'assignment_mode', 'created_at'
    ]
    search_fields = ['title', 'description', 'creator__real_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'task_type', 'priority')
        }),
        ('创建信息', {
            'fields': ('creator', 'creator_department', 'profession')
        }),
        ('分配信息', {
            'fields': ('assignment_mode',)
        }),
        ('时间信息', {
            'fields': ('start_date', 'due_date', 'estimated_hours')
        }),
        ('状态信息', {
            'fields': ('status', 'has_attachments')
        }),
    )
    
    readonly_fields = ['creator', 'creator_department', 'has_attachments']
    
    def is_overdue(self, obj):
        """是否逾期"""
        if obj.is_overdue:
            return format_html('<span style="color: red;">是</span>')
        return '否'
    is_overdue.short_description = '是否逾期'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'creator', 'creator_department', 'profession'
        )


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    """任务分配管理"""
    list_display = [
        'task', 'assignee', 'assignee_department', 'role', 
        'is_primary', 'status', 'assigned_at'
    ]
    list_filter = ['role', 'is_primary', 'status', 'assigned_at']
    search_fields = ['task__title', 'assignee__real_name']
    ordering = ['-assigned_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'task', 'assignee', 'assignee_department'
        )


@admin.register(TaskExecution)
class TaskExecutionAdmin(admin.ModelAdmin):
    """任务执行管理"""
    list_display = [
        'assignment', 'status', 'progress_percentage', 
        'actual_hours', 'started_at', 'completed_at'
    ]
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['assignment__task__title', 'assignment__assignee__real_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'assignment__task', 'assignment__assignee'
        )


@admin.register(TaskReview)
class TaskReviewAdmin(admin.ModelAdmin):
    """任务评价管理"""
    list_display = [
        'task', 'reviewer', 'rating', 'quality_rating', 
        'timeliness_rating', 'overall_rating', 'is_satisfied', 'reviewed_at'
    ]
    list_filter = ['rating', 'is_satisfied', 'reviewed_at']
    search_fields = ['task__title', 'reviewer__real_name']
    ordering = ['-reviewed_at']
    
    def overall_rating(self, obj):
        """综合评分"""
        return f"{obj.overall_rating:.1f}"
    overall_rating.short_description = '综合评分'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'reviewer')


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    """任务附件管理"""
    list_display = [
        'task', 'original_name', 'file_size_display', 
        'attachment_type', 'uploader', 'uploaded_at'
    ]
    list_filter = ['attachment_type', 'uploaded_at']
    search_fields = ['task__title', 'original_name', 'uploader__real_name']
    ordering = ['-uploaded_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'uploader')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    """任务评论管理"""
    list_display = ['task', 'author', 'comment_type', 'content_preview', 'created_at']
    list_filter = ['comment_type', 'created_at']
    search_fields = ['task__title', 'author__real_name', 'content']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        """内容预览"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容预览'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'author')


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    """任务模板管理"""
    list_display = [
        'name', 'task_type', 'priority', 'department', 
        'profession', 'status', 'usage_count', 'created_at'
    ]
    list_filter = ['task_type', 'priority', 'status', 'department', 'created_at']
    search_fields = ['name', 'description', 'creator__real_name']
    ordering = ['-usage_count', '-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'creator', 'department', 'profession'
        )
