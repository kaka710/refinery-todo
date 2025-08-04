"""
集成相关视图
"""
import logging
from django.db.models import Q, Count, Avg
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    ShihuatongIntegration, ShihuatongMessage, ShihuatongUserMapping, IntegrationLog
)
from .serializers import (
    ShihuatongIntegrationSerializer, ShihuatongIntegrationSimpleSerializer,
    ShihuatongMessageSerializer, ShihuatongMessageCreateSerializer,
    ShihuatongUserMappingSerializer, ShihuatongUserMappingCreateSerializer,
    IntegrationLogSerializer, ShihuatongStatsSerializer, SendMessageSerializer
)
from .services import ShihuatongService
from .tasks import send_shihuatong_message_task
from apps.users.permissions import IsAdminUser

logger = logging.getLogger(__name__)


class ShihuatongIntegrationViewSet(ModelViewSet):
    """石化通集成管理视图集"""
    queryset = ShihuatongIntegration.objects.all()
    serializer_class = ShihuatongIntegrationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'last_used_at', 'success_rate']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'list':
            return ShihuatongIntegrationSimpleSerializer
        return ShihuatongIntegrationSerializer
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """测试集成连接"""
        integration = self.get_object()
        
        try:
            service = ShihuatongService(integration.id)
            health_status = service.health_check()
            
            return Response(health_status)
        except Exception as e:
            logger.error(f"测试石化通连接失败: {e}")
            return Response(
                {'error': f'连接测试失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def send_test_message(self, request, pk=None):
        """发送测试消息"""
        integration = self.get_object()
        
        hook_token = request.data.get('hook_token')
        if not hook_token:
            return Response(
                {'error': '请提供Hook Token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = ShihuatongService(integration.id)
            message = service.send_message(
                hook_token=hook_token,
                title='测试消息',
                content='这是一条来自海南炼化Todo系统的测试消息',
                message_type='text'
            )
            
            serializer = ShihuatongMessageSerializer(message)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"发送测试消息失败: {e}")
            return Response(
                {'error': f'发送失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取石化通统计信息"""
        # 总集成数
        total_integrations = ShihuatongIntegration.objects.count()
        active_integrations = ShihuatongIntegration.objects.filter(
            status=ShihuatongIntegration.IntegrationStatus.ACTIVE
        ).count()
        
        # 消息统计
        total_messages = ShihuatongMessage.objects.count()
        success_messages = ShihuatongMessage.objects.filter(
            status=ShihuatongMessage.MessageStatus.SUCCESS
        ).count()
        failed_messages = ShihuatongMessage.objects.filter(
            status=ShihuatongMessage.MessageStatus.FAILED
        ).count()
        
        success_rate = (success_messages / total_messages * 100) if total_messages > 0 else 0
        
        # 最近消息
        recent_messages = ShihuatongMessage.objects.order_by('-created_at')[:10]
        
        stats_data = {
            'total_integrations': total_integrations,
            'active_integrations': active_integrations,
            'total_messages': total_messages,
            'success_messages': success_messages,
            'failed_messages': failed_messages,
            'success_rate': round(success_rate, 2),
            'recent_messages': recent_messages
        }
        
        serializer = ShihuatongStatsSerializer(stats_data)
        return Response(serializer.data)


class ShihuatongMessageViewSet(ModelViewSet):
    """石化通消息管理视图集"""
    queryset = ShihuatongMessage.objects.all()
    serializer_class = ShihuatongMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['integration', 'message_type', 'status', 'related_task']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['create', 'send_message']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'create':
            return ShihuatongMessageCreateSerializer
        elif self.action == 'send_message':
            return SendMessageSerializer
        return ShihuatongMessageSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return ShihuatongMessage.objects.all()
        else:
            # 普通用户只能看到与自己相关的消息
            return ShihuatongMessage.objects.filter(
                Q(related_task__creator=user) |
                Q(related_task__assignments__assignee=user) |
                Q(related_notification__recipient=user)
            ).distinct()
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """发送石化通消息"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        try:
            # 异步发送消息
            task_result = send_shihuatong_message_task.delay(
                hook_token=data['hook_token'],
                title=data['title'],
                content=data['content'],
                message_type=data.get('message_type', 'text'),
                mention_all=data.get('mention_all', False),
                user_ids=data.get('user_ids', []),
                related_task_id=str(data['related_task_id']) if data.get('related_task_id') else None,
                integration_id=data.get('integration_id')
            )
            
            return Response({
                'message': '消息发送任务已提交',
                'task_id': task_result.id
            })
        except Exception as e:
            logger.error(f"提交消息发送任务失败: {e}")
            return Response(
                {'error': f'发送失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """重试发送消息"""
        message = self.get_object()
        
        if not message.can_retry:
            return Response(
                {'error': '该消息不能重试'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = ShihuatongService(message.integration.id)
            success = service.retry_failed_message(str(message.id))
            
            if success:
                return Response({'message': '重试成功'})
            else:
                return Response(
                    {'error': '重试失败'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"重试消息失败: {e}")
            return Response(
                {'error': f'重试失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShihuatongUserMappingViewSet(ModelViewSet):
    """石化通用户映射管理视图集"""
    queryset = ShihuatongUserMapping.objects.all()
    serializer_class = ShihuatongUserMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user']
    search_fields = ['shihuatong_username', 'shihuatong_display_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'create':
            return ShihuatongUserMappingCreateSerializer
        return ShihuatongUserMappingSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return ShihuatongUserMapping.objects.all()
        else:
            # 普通用户只能看到自己的映射
            return ShihuatongUserMapping.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def my_mapping(self, request):
        """获取当前用户的映射"""
        user = request.user
        
        try:
            mapping = ShihuatongUserMapping.objects.get(user=user)
            serializer = self.get_serializer(mapping)
            return Response(serializer.data)
        except ShihuatongUserMapping.DoesNotExist:
            return Response(
                {'error': '用户没有石化通映射配置'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """验证映射"""
        mapping = self.get_object()
        
        # 这里可以添加验证逻辑，比如发送验证消息等
        # 暂时直接标记为已验证
        from django.utils import timezone
        
        mapping.status = ShihuatongUserMapping.MappingStatus.ACTIVE
        mapping.verified_at = timezone.now()
        mapping.save(update_fields=['status', 'verified_at'])
        
        return Response({'message': '映射已验证'})


class IntegrationLogViewSet(ModelViewSet):
    """集成日志视图集"""
    queryset = IntegrationLog.objects.all()
    serializer_class = IntegrationLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['integration', 'level', 'operation_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    http_method_names = ['get']  # 只允许查看
