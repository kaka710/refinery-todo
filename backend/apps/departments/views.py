"""
部门相关视图
"""
from django.db.models import Count, Q
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Department, Profession, DepartmentCollaboration
from .serializers import (
    DepartmentSerializer, DepartmentTreeSerializer, DepartmentSimpleSerializer,
    ProfessionSerializer, ProfessionSimpleSerializer,
    DepartmentCollaborationSerializer, DepartmentStatsSerializer
)
from apps.users.permissions import IsAdminUser, IsDepartmentManager


class DepartmentViewSet(ModelViewSet):
    """部门管理视图集"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'status', 'parent']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['level', 'sort_order', 'name', 'created_at']
    ordering = ['level', 'sort_order', 'name']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'tree':
            return DepartmentTreeSerializer
        elif self.action in ['list'] and hasattr(self.request, 'query_params') and self.request.query_params.get('simple'):
            return DepartmentSimpleSerializer
        return DepartmentSerializer
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取部门树形结构"""
        # 只获取根部门
        root_departments = Department.objects.filter(
            parent=None,
            status=Department.DepartmentStatus.ACTIVE
        ).order_by('sort_order', 'name')
        
        serializer = self.get_serializer(root_departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """获取部门的直接子部门"""
        department = self.get_object()
        children = department.children.filter(
            status=Department.DepartmentStatus.ACTIVE
        ).order_by('sort_order', 'name')
        
        serializer = DepartmentSerializer(children, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """获取部门用户"""
        department = self.get_object()
        users = department.users.filter(status='active')
        
        from apps.users.serializers import UserSimpleSerializer
        serializer = UserSimpleSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """获取部门统计信息"""
        department = self.get_object()
        
        # 统计用户数量
        total_users = department.users.count()
        active_users = department.users.filter(status='active').count()
        
        # 统计任务数量
        from apps.tasks.models import Task
        tasks = Task.objects.filter(creator_department=department)
        total_tasks = tasks.count()
        pending_tasks = tasks.filter(status__in=['pending', 'accepted', 'in_progress']).count()
        completed_tasks = tasks.filter(status='completed').count()
        overdue_tasks = tasks.filter(status='overdue').count()
        
        stats_data = {
            'department_id': department.id,
            'department_name': department.name,
            'total_users': total_users,
            'active_users': active_users,
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks
        }
        
        serializer = DepartmentStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_departments(self, request):
        """获取当前用户管理的部门"""
        user = request.user
        departments = user.get_managed_departments()
        
        serializer = DepartmentSimpleSerializer(departments, many=True)
        return Response(serializer.data)


class ProfessionViewSet(ModelViewSet):
    """专业管理视图集"""
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'status', 'manager']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['department', 'sort_order', 'name']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsDepartmentManager]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'list' and hasattr(self.request, 'query_params') and self.request.query_params.get('simple'):
            return ProfessionSimpleSerializer
        return ProfessionSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return Profession.objects.all()
        elif user.is_dept_manager and user.department:
            # 部门负责人只能看到自己部门的专业
            return Profession.objects.filter(department=user.department)
        else:
            # 普通用户可以看到所有专业（只读）
            return Profession.objects.filter(status=Profession.ProfessionStatus.ACTIVE)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """获取专业相关用户"""
        profession = self.get_object()
        users = profession.get_users()
        
        from apps.users.serializers import UserSimpleSerializer
        serializer = UserSimpleSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """按部门获取专业列表"""
        department_id = getattr(request, 'query_params', request.GET).get('department_id')
        if not department_id:
            return Response({'error': '请提供部门ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        professions = Profession.objects.filter(
            department_id=department_id,
            status=Profession.ProfessionStatus.ACTIVE
        ).order_by('sort_order', 'name')
        
        serializer = ProfessionSimpleSerializer(professions, many=True)
        return Response(serializer.data)


class DepartmentCollaborationViewSet(ModelViewSet):
    """部门协作关系管理视图集"""
    queryset = DepartmentCollaboration.objects.all()
    serializer_class = DepartmentCollaborationSerializer
    permission_classes = [IsDepartmentManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['primary_department', 'secondary_department', 'collaboration_type', 'is_active']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return DepartmentCollaboration.objects.all()
        elif user.is_dept_manager and user.department:
            # 部门负责人只能看到与自己部门相关的协作关系
            return DepartmentCollaboration.objects.filter(
                Q(primary_department=user.department) | 
                Q(secondary_department=user.department)
            )
        else:
            return DepartmentCollaboration.objects.none()
    
    @action(detail=False, methods=['get'])
    def my_collaborations(self, request):
        """获取当前用户部门的协作关系"""
        user = request.user
        if not user.department:
            return Response([])
        
        collaborations = DepartmentCollaboration.objects.filter(
            Q(primary_department=user.department) | 
            Q(secondary_department=user.department),
            is_active=True
        )
        
        serializer = self.get_serializer(collaborations, many=True)
        return Response(serializer.data)
