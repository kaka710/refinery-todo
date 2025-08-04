"""
任务相关视图
"""
import logging
from django.db.models import Q, Count, Avg
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Task, TaskAssignment, TaskExecution, TaskReview, 
    TaskAttachment, TaskComment, TaskTemplate
)
from .serializers import (
    TaskSerializer, TaskSimpleSerializer, TaskCreateSerializer,
    TaskAssignmentSerializer, TaskExecutionSerializer, TaskReviewSerializer,
    TaskAttachmentSerializer, TaskCommentSerializer, TaskTemplateSerializer
)
from apps.users.permissions import (
    CanCreateTask, IsTaskCreatorOrAssignee, IsTaskAssignee
)

logger = logging.getLogger(__name__)


class TaskViewSet(ModelViewSet):
    """任务管理视图集"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'task_type', 'priority', 'status', 'creator', 'creator_department',
        'profession', 'assignment_mode'
    ]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action == 'create':
            permission_classes = [CanCreateTask]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsTaskCreatorOrAssignee]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTaskCreatorOrAssignee]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'list':
            return TaskSimpleSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return Task.objects.all()
        
        # 构建查询条件
        q_objects = Q()
        
        # 用户创建的任务
        q_objects |= Q(creator=user)
        
        # 用户被分配的任务
        q_objects |= Q(assignments__assignee=user)
        
        # 部门负责人可以看到本部门的任务
        if user.is_dept_manager and user.department:
            q_objects |= Q(creator_department=user.department)
        
        return Task.objects.filter(q_objects).distinct()
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """获取我的任务"""
        user = request.user
        
        # 我创建的任务
        created_tasks = Task.objects.filter(creator=user)
        
        # 分配给我的任务
        assigned_tasks = Task.objects.filter(assignments__assignee=user)
        
        # 合并并去重
        all_tasks = (created_tasks | assigned_tasks).distinct()
        
        # 应用过滤和排序
        filtered_tasks = self.filter_queryset(all_tasks)
        
        page = self.paginate_queryset(filtered_tasks)
        if page is not None:
            serializer = TaskSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskSimpleSerializer(filtered_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def assigned_to_me(self, request):
        """获取分配给我的任务"""
        user = request.user
        
        tasks = Task.objects.filter(
            assignments__assignee=user
        ).distinct()
        
        # 根据状态过滤
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(assignments__assignee=user, assignments__status=status_filter)
        
        filtered_tasks = self.filter_queryset(tasks)
        
        page = self.paginate_queryset(filtered_tasks)
        if page is not None:
            serializer = TaskSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskSimpleSerializer(filtered_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def created_by_me(self, request):
        """获取我创建的任务"""
        user = request.user
        
        tasks = Task.objects.filter(creator=user)
        filtered_tasks = self.filter_queryset(tasks)
        
        page = self.paginate_queryset(filtered_tasks)
        if page is not None:
            serializer = TaskSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskSimpleSerializer(filtered_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """获取逾期任务"""
        user = request.user
        
        # 获取用户相关的逾期任务
        base_queryset = self.get_queryset()
        overdue_tasks = base_queryset.filter(
            due_date__lt=timezone.now(),
            status__in=[
                Task.TaskStatus.PENDING,
                Task.TaskStatus.ACCEPTED,
                Task.TaskStatus.IN_PROGRESS,
                Task.TaskStatus.OVERDUE
            ]
        )
        
        filtered_tasks = self.filter_queryset(overdue_tasks)
        
        page = self.paginate_queryset(filtered_tasks)
        if page is not None:
            serializer = TaskSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskSimpleSerializer(filtered_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布任务"""
        task = self.get_object()
        
        if task.creator != request.user:
            return Response(
                {'error': '只有任务创建者可以发布任务'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if task.status != Task.TaskStatus.DRAFT:
            return Response(
                {'error': '只有草稿状态的任务可以发布'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = Task.TaskStatus.PENDING
        task.published_at = timezone.now()
        task.save(update_fields=['status', 'published_at'])
        
        return Response({'message': '任务已发布'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消任务"""
        task = self.get_object()
        
        if task.creator != request.user and not request.user.is_admin:
            return Response(
                {'error': '只有任务创建者或管理员可以取消任务'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if task.status in [Task.TaskStatus.COMPLETED, Task.TaskStatus.REVIEWED]:
            return Response(
                {'error': '已完成的任务不能取消'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = Task.TaskStatus.CANCELLED
        task.save(update_fields=['status'])
        
        return Response({'message': '任务已取消'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取任务统计信息"""
        user = request.user
        base_queryset = self.get_queryset()
        
        # 总任务数
        total_tasks = base_queryset.count()
        
        # 按状态统计
        status_stats = {}
        for status_choice in Task.TaskStatus.choices:
            status_code = status_choice[0]
            status_name = status_choice[1]
            count = base_queryset.filter(status=status_code).count()
            status_stats[status_code] = {
                'name': status_name,
                'count': count
            }
        
        # 按优先级统计
        priority_stats = {}
        for priority_choice in Task.Priority.choices:
            priority_code = priority_choice[0]
            priority_name = priority_choice[1]
            count = base_queryset.filter(priority=priority_code).count()
            priority_stats[priority_code] = {
                'name': priority_name,
                'count': count
            }
        
        # 逾期任务数
        overdue_count = base_queryset.filter(
            due_date__lt=timezone.now(),
            status__in=[
                Task.TaskStatus.PENDING,
                Task.TaskStatus.ACCEPTED,
                Task.TaskStatus.IN_PROGRESS,
                Task.TaskStatus.OVERDUE
            ]
        ).count()
        
        # 我的任务统计
        my_assigned_tasks = base_queryset.filter(assignments__assignee=user).distinct()
        my_pending_tasks = my_assigned_tasks.filter(
            assignments__assignee=user,
            assignments__status__in=[
                TaskAssignment.AssignmentStatus.PENDING,
                TaskAssignment.AssignmentStatus.ACCEPTED,
                TaskAssignment.AssignmentStatus.IN_PROGRESS
            ]
        ).count()
        
        return Response({
            'total_tasks': total_tasks,
            'status_stats': status_stats,
            'priority_stats': priority_stats,
            'overdue_count': overdue_count,
            'my_pending_tasks': my_pending_tasks
        })


class TaskAssignmentViewSet(ModelViewSet):
    """任务分配管理视图集"""
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['task', 'assignee', 'status', 'role', 'is_primary']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']

    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsTaskAssignee]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskAssignment.objects.all()

        # 用户只能看到自己相关的任务分配
        return TaskAssignment.objects.filter(
            Q(assignee=user) | Q(task__creator=user)
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """接受任务分配"""
        assignment = self.get_object()

        if assignment.assignee != request.user:
            return Response(
                {'error': '只能接受分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if assignment.status != TaskAssignment.AssignmentStatus.PENDING:
            return Response(
                {'error': '只有待接收状态的任务可以接受'},
                status=status.HTTP_400_BAD_REQUEST
            )

        assignment.status = TaskAssignment.AssignmentStatus.ACCEPTED
        assignment.accepted_at = timezone.now()
        assignment.save(update_fields=['status', 'accepted_at'])

        # 创建执行记录
        TaskExecution.objects.get_or_create(
            assignment=assignment,
            defaults={'status': TaskExecution.ExecutionStatus.NOT_STARTED}
        )

        return Response({'message': '任务已接受'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝任务分配"""
        assignment = self.get_object()

        if assignment.assignee != request.user:
            return Response(
                {'error': '只能拒绝分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if assignment.status != TaskAssignment.AssignmentStatus.PENDING:
            return Response(
                {'error': '只有待接收状态的任务可以拒绝'},
                status=status.HTTP_400_BAD_REQUEST
            )

        assignment.status = TaskAssignment.AssignmentStatus.REJECTED
        assignment.save(update_fields=['status'])

        return Response({'message': '任务已拒绝'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成任务分配"""
        assignment = self.get_object()

        if assignment.assignee != request.user:
            return Response(
                {'error': '只能完成分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if assignment.status not in [
            TaskAssignment.AssignmentStatus.ACCEPTED,
            TaskAssignment.AssignmentStatus.IN_PROGRESS
        ]:
            return Response(
                {'error': '只有已接收或进行中的任务可以完成'},
                status=status.HTTP_400_BAD_REQUEST
            )

        assignment.status = TaskAssignment.AssignmentStatus.COMPLETED
        assignment.completed_at = timezone.now()
        assignment.save(update_fields=['status', 'completed_at'])

        # 更新执行记录
        if hasattr(assignment, 'execution'):
            assignment.execution.status = TaskExecution.ExecutionStatus.COMPLETED
            assignment.execution.completed_at = timezone.now()
            assignment.execution.progress_percentage = 100
            assignment.execution.save()

        return Response({'message': '任务已完成'})


class TaskExecutionViewSet(ModelViewSet):
    """任务执行管理视图集"""
    queryset = TaskExecution.objects.all()
    serializer_class = TaskExecutionSerializer
    permission_classes = [IsTaskAssignee]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'assignment__task', 'assignment__assignee']
    ordering_fields = ['updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskExecution.objects.all()

        # 用户只能看到自己的执行记录
        return TaskExecution.objects.filter(assignment__assignee=user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """开始执行任务"""
        execution = self.get_object()

        if execution.assignment.assignee != request.user:
            return Response(
                {'error': '只能开始执行分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if execution.status != TaskExecution.ExecutionStatus.NOT_STARTED:
            return Response(
                {'error': '只有未开始的任务可以开始执行'},
                status=status.HTTP_400_BAD_REQUEST
            )

        execution.status = TaskExecution.ExecutionStatus.IN_PROGRESS
        execution.started_at = timezone.now()
        execution.save(update_fields=['status', 'started_at'])

        # 更新分配状态
        assignment = execution.assignment
        if assignment.status == TaskAssignment.AssignmentStatus.ACCEPTED:
            assignment.status = TaskAssignment.AssignmentStatus.IN_PROGRESS
            assignment.save(update_fields=['status'])

        return Response({'message': '任务执行已开始'})

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """暂停执行任务"""
        execution = self.get_object()

        if execution.assignment.assignee != request.user:
            return Response(
                {'error': '只能暂停分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if execution.status != TaskExecution.ExecutionStatus.IN_PROGRESS:
            return Response(
                {'error': '只有进行中的任务可以暂停'},
                status=status.HTTP_400_BAD_REQUEST
            )

        execution.status = TaskExecution.ExecutionStatus.PAUSED
        execution.save(update_fields=['status'])

        return Response({'message': '任务执行已暂停'})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """恢复执行任务"""
        execution = self.get_object()

        if execution.assignment.assignee != request.user:
            return Response(
                {'error': '只能恢复分配给自己的任务'},
                status=status.HTTP_403_FORBIDDEN
            )

        if execution.status != TaskExecution.ExecutionStatus.PAUSED:
            return Response(
                {'error': '只有暂停的任务可以恢复'},
                status=status.HTTP_400_BAD_REQUEST
            )

        execution.status = TaskExecution.ExecutionStatus.IN_PROGRESS
        execution.save(update_fields=['status'])

        return Response({'message': '任务执行已恢复'})


class TaskReviewViewSet(ModelViewSet):
    """任务评价管理视图集"""
    queryset = TaskReview.objects.all()
    serializer_class = TaskReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['task', 'reviewer', 'rating', 'is_satisfied']
    ordering_fields = ['reviewed_at']
    ordering = ['-reviewed_at']

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskReview.objects.all()

        # 用户只能看到自己创建的任务的评价或自己的评价
        return TaskReview.objects.filter(
            Q(task__creator=user) | Q(reviewer=user)
        )

    def perform_create(self, serializer):
        """创建评价时检查权限"""
        task = serializer.validated_data['task']
        user = self.request.user

        # 只有任务创建者可以评价
        if task.creator != user:
            raise serializers.ValidationError('只有任务创建者可以进行评价')

        # 只有已完成的任务可以评价
        if task.status != Task.TaskStatus.COMPLETED:
            raise serializers.ValidationError('只有已完成的任务可以评价')

        # 检查是否已经评价过
        if TaskReview.objects.filter(task=task).exists():
            raise serializers.ValidationError('该任务已经评价过了')

        serializer.save()


class TaskAttachmentViewSet(ModelViewSet):
    """任务附件管理视图集"""
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsTaskCreatorOrAssignee]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['task', 'attachment_type', 'uploader']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskAttachment.objects.all()

        # 用户只能看到自己相关任务的附件
        return TaskAttachment.objects.filter(
            Q(task__creator=user) |
            Q(task__assignments__assignee=user) |
            Q(uploader=user)
        ).distinct()

    def perform_create(self, serializer):
        """创建附件时自动更新任务的附件标志"""
        attachment = serializer.save()

        # 更新任务的附件标志
        task = attachment.task
        if not task.has_attachments:
            task.has_attachments = True
            task.save(update_fields=['has_attachments'])


class TaskCommentViewSet(ModelViewSet):
    """任务评论管理视图集"""
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [IsTaskCreatorOrAssignee]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['task', 'author', 'comment_type', 'parent']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskComment.objects.all()

        # 用户只能看到自己相关任务的评论
        return TaskComment.objects.filter(
            Q(task__creator=user) |
            Q(task__assignments__assignee=user) |
            Q(author=user)
        ).distinct()


class TaskTemplateViewSet(ModelViewSet):
    """任务模板管理视图集"""
    queryset = TaskTemplate.objects.all()
    serializer_class = TaskTemplateSerializer
    permission_classes = [CanCreateTask]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'profession', 'status', 'task_type']
    search_fields = ['name', 'description']
    ordering_fields = ['usage_count', 'created_at']
    ordering = ['-usage_count', '-created_at']

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        if user.is_admin:
            return TaskTemplate.objects.all()
        elif user.department:
            # 用户只能看到自己部门的模板和公共模板
            return TaskTemplate.objects.filter(
                Q(department=user.department) | Q(department=None),
                status=TaskTemplate.TemplateStatus.ACTIVE
            )
        else:
            return TaskTemplate.objects.filter(
                department=None,
                status=TaskTemplate.TemplateStatus.ACTIVE
            )

    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """使用模板创建任务"""
        template = self.get_object()

        # 获取请求参数
        title = request.data.get('title')
        description = request.data.get('description')
        start_date = request.data.get('start_date')
        due_date = request.data.get('due_date')
        assignee_ids = request.data.get('assignee_ids', [])

        if not all([title, start_date, due_date, assignee_ids]):
            return Response(
                {'error': '请提供完整的任务信息'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 使用模板创建任务
            task = template.create_task_from_template(
                creator=request.user,
                title=title,
                description=description,
                start_date=start_date,
                due_date=due_date
            )

            # 创建任务分配
            from apps.users.models import User
            for assignee_id in assignee_ids:
                try:
                    assignee = User.objects.get(id=assignee_id)
                    TaskAssignment.objects.create(
                        task=task,
                        assignee=assignee,
                        assignee_department=assignee.department
                    )
                except User.DoesNotExist:
                    continue

            # 返回创建的任务
            task_serializer = TaskSerializer(task)
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"使用模板创建任务失败: {e}")
            return Response(
                {'error': '创建任务失败'},
                status=status.HTTP_400_BAD_REQUEST
            )
