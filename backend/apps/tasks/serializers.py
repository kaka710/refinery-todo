"""
任务相关序列化器
"""
from rest_framework import serializers
from django.utils import timezone

from .models import (
    Task, TaskAssignment, TaskExecution, TaskReview, 
    TaskAttachment, TaskComment, TaskTemplate
)
from apps.users.serializers import UserSimpleSerializer
from apps.departments.serializers import DepartmentSimpleSerializer, ProfessionSimpleSerializer


class TaskAttachmentSerializer(serializers.ModelSerializer):
    """任务附件序列化器"""
    uploader_name = serializers.CharField(source='uploader.real_name', read_only=True)
    file_size_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = [
            'id', 'file', 'original_name', 'file_size', 'file_size_display',
            'file_type', 'attachment_type', 'description',
            'uploader', 'uploader_name', 'uploaded_at'
        ]
        read_only_fields = ['uploader', 'file_size', 'file_type', 'uploaded_at']
    
    def create(self, validated_data):
        """创建附件时自动设置文件信息"""
        file_obj = validated_data['file']
        validated_data['original_name'] = file_obj.name
        validated_data['file_size'] = file_obj.size
        validated_data['file_type'] = file_obj.content_type or 'application/octet-stream'
        validated_data['uploader'] = self.context['request'].user
        
        return super().create(validated_data)


class TaskCommentSerializer(serializers.ModelSerializer):
    """任务评论序列化器"""
    author = UserSimpleSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskComment
        fields = [
            'id', 'content', 'comment_type', 'author', 'parent',
            'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        """获取回复"""
        if obj.parent is None:  # 只为顶级评论获取回复
            replies = obj.replies.all().order_by('created_at')
            return TaskCommentSerializer(replies, many=True, context=self.context).data
        return []
    
    def create(self, validated_data):
        """创建评论时自动设置作者"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class TaskExecutionSerializer(serializers.ModelSerializer):
    """任务执行序列化器"""
    
    class Meta:
        model = TaskExecution
        fields = [
            'id', 'status', 'progress_percentage', 'result_description',
            'actual_hours', 'issues_encountered', 'risks_identified',
            'started_at', 'completed_at', 'updated_at'
        ]
        read_only_fields = ['started_at', 'completed_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """更新执行状态时自动设置时间"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # 如果状态从未开始变为进行中，设置开始时间
        if (old_status == TaskExecution.ExecutionStatus.NOT_STARTED and 
            new_status == TaskExecution.ExecutionStatus.IN_PROGRESS and
            not instance.started_at):
            validated_data['started_at'] = timezone.now()
        
        # 如果状态变为已完成，设置完成时间
        if (new_status == TaskExecution.ExecutionStatus.COMPLETED and
            old_status != TaskExecution.ExecutionStatus.COMPLETED):
            validated_data['completed_at'] = timezone.now()
            validated_data['progress_percentage'] = 100
        
        return super().update(instance, validated_data)


class TaskAssignmentSerializer(serializers.ModelSerializer):
    """任务分配序列化器"""
    assignee = UserSimpleSerializer(read_only=True)
    assignee_department = DepartmentSimpleSerializer(read_only=True)
    execution = TaskExecutionSerializer(read_only=True)
    
    class Meta:
        model = TaskAssignment
        fields = [
            'id', 'assignee', 'assignee_department', 'role', 'is_primary',
            'status', 'assignment_note', 'execution',
            'assigned_at', 'accepted_at', 'completed_at'
        ]
        read_only_fields = ['assigned_at', 'accepted_at', 'completed_at']
    
    def update(self, instance, validated_data):
        """更新分配状态时自动设置时间"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # 如果状态变为已接收，设置接收时间
        if (new_status == TaskAssignment.AssignmentStatus.ACCEPTED and
            old_status != TaskAssignment.AssignmentStatus.ACCEPTED):
            validated_data['accepted_at'] = timezone.now()
        
        # 如果状态变为已完成，设置完成时间
        if (new_status == TaskAssignment.AssignmentStatus.COMPLETED and
            old_status != TaskAssignment.AssignmentStatus.COMPLETED):
            validated_data['completed_at'] = timezone.now()
        
        return super().update(instance, validated_data)


class TaskReviewSerializer(serializers.ModelSerializer):
    """任务评价序列化器"""
    reviewer = UserSimpleSerializer(read_only=True)
    overall_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = TaskReview
        fields = [
            'id', 'reviewer', 'rating', 'quality_rating', 'timeliness_rating',
            'overall_rating', 'comments', 'suggestions', 'is_satisfied',
            'reviewed_at'
        ]
        read_only_fields = ['reviewer', 'reviewed_at']
    
    def create(self, validated_data):
        """创建评价时自动设置评价人"""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    """任务序列化器"""
    creator = UserSimpleSerializer(read_only=True)
    creator_department = DepartmentSimpleSerializer(read_only=True)
    profession = ProfessionSimpleSerializer(read_only=True)
    assignments = TaskAssignmentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    review = TaskReviewSerializer(read_only=True)
    
    # 计算字段
    is_overdue = serializers.BooleanField(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_type', 'priority',
            'creator', 'creator_department', 'profession',
            'assignment_mode', 'start_date', 'due_date', 'estimated_hours',
            'status', 'has_attachments', 'assignments', 'attachments',
            'comments', 'review', 'is_overdue', 'progress_percentage',
            'created_at', 'updated_at', 'published_at', 'completed_at'
        ]
        read_only_fields = [
            'creator', 'creator_department', 'has_attachments',
            'created_at', 'updated_at', 'published_at', 'completed_at'
        ]
    
    def create(self, validated_data):
        """创建任务时自动设置创建者信息"""
        user = self.context['request'].user
        validated_data['creator'] = user
        validated_data['creator_department'] = user.department
        
        return super().create(validated_data)
    
    def validate(self, attrs):
        """验证任务数据"""
        start_date = attrs.get('start_date')
        due_date = attrs.get('due_date')
        
        if start_date and due_date and start_date >= due_date:
            raise serializers.ValidationError('开始时间必须早于截止时间')
        
        return attrs


class TaskSimpleSerializer(serializers.ModelSerializer):
    """任务简单序列化器"""
    creator_name = serializers.CharField(source='creator.real_name', read_only=True)
    department_name = serializers.CharField(source='creator_department.name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'task_type', 'priority', 'status',
            'creator_name', 'department_name', 'start_date', 'due_date',
            'is_overdue', 'progress_percentage', 'created_at'
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    """任务创建序列化器"""
    assignee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        help_text='执行人ID列表'
    )
    primary_assignee_id = serializers.IntegerField(
        write_only=True,
        required=False,
        help_text='主要执行人ID（一对多模式时必填）'
    )
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'task_type', 'priority',
            'profession', 'assignment_mode', 'start_date', 'due_date',
            'estimated_hours', 'assignee_ids', 'primary_assignee_id'
        ]
    
    def validate(self, attrs):
        """验证任务创建数据"""
        attrs = super().validate(attrs)
        
        assignee_ids = attrs.get('assignee_ids', [])
        assignment_mode = attrs.get('assignment_mode')
        primary_assignee_id = attrs.get('primary_assignee_id')
        
        if not assignee_ids:
            raise serializers.ValidationError('必须指定至少一个执行人')
        
        if assignment_mode == Task.AssignmentMode.ONE_TO_MANY and len(assignee_ids) > 1:
            if not primary_assignee_id:
                raise serializers.ValidationError('一对多模式必须指定主要执行人')
            if primary_assignee_id not in assignee_ids:
                raise serializers.ValidationError('主要执行人必须在执行人列表中')
        
        return attrs
    
    def create(self, validated_data):
        """创建任务和分配"""
        assignee_ids = validated_data.pop('assignee_ids')
        primary_assignee_id = validated_data.pop('primary_assignee_id', None)
        
        # 创建任务
        user = self.context['request'].user
        validated_data['creator'] = user
        validated_data['creator_department'] = user.department
        
        task = super().create(validated_data)
        
        # 创建任务分配
        from apps.users.models import User
        
        for assignee_id in assignee_ids:
            try:
                assignee = User.objects.get(id=assignee_id)
                is_primary = (assignee_id == primary_assignee_id)
                
                TaskAssignment.objects.create(
                    task=task,
                    assignee=assignee,
                    assignee_department=assignee.department,
                    role=TaskAssignment.AssignmentRole.PRIMARY if is_primary else TaskAssignment.AssignmentRole.COLLABORATOR,
                    is_primary=is_primary
                )
            except User.DoesNotExist:
                continue
        
        return task


class TaskTemplateSerializer(serializers.ModelSerializer):
    """任务模板序列化器"""
    creator = UserSimpleSerializer(read_only=True)
    department = DepartmentSimpleSerializer(read_only=True)
    profession = ProfessionSimpleSerializer(read_only=True)
    
    class Meta:
        model = TaskTemplate
        fields = [
            'id', 'name', 'description', 'title_template', 'description_template',
            'task_type', 'priority', 'estimated_hours', 'creator', 'department',
            'profession', 'status', 'usage_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'department', 'usage_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """创建模板时自动设置创建者信息"""
        user = self.context['request'].user
        validated_data['creator'] = user
        validated_data['department'] = user.department
        
        return super().create(validated_data)
