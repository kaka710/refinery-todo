"""
通知相关视图
"""
import logging
from django.db.models import Q, Count
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Notification, NotificationTemplate, NotificationLog, UserNotificationSettings
)
from .serializers import (
    NotificationSerializer, NotificationSimpleSerializer, NotificationTemplateSerializer,
    NotificationLogSerializer, UserNotificationSettingsSerializer,
    NotificationCreateSerializer, NotificationStatsSerializer
)
from .services import NotificationService
from apps.users.permissions import IsAdminUser

logger = logging.getLogger(__name__)


class NotificationViewSet(ModelViewSet):
    """通知管理视图集"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['notification_type', 'status', 'sender']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'list':
            return NotificationSimpleSerializer
        elif self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return Notification.objects.all()
        else:
            # 普通用户只能看到自己的通知
            return Notification.objects.filter(recipient=user)
    
    def create(self, request, *args, **kwargs):
        """创建通知"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        recipient_ids = data.pop('recipient_ids')
        
        # 为每个接收者创建通知
        created_notifications = []
        for recipient_id in recipient_ids:
            try:
                notification = NotificationService.create_notification(
                    recipient_id=recipient_id,
                    sender_id=request.user.id,
                    **data
                )
                created_notifications.append(notification)
            except Exception as e:
                logger.error(f"为用户 {recipient_id} 创建通知失败: {e}")
                continue
        
        if created_notifications:
            response_serializer = NotificationSerializer(
                created_notifications, many=True
            )
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': '创建通知失败'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """获取未读通知"""
        user = request.user
        unread_notifications = Notification.objects.filter(
            recipient=user,
            status=Notification.NotificationStatus.UNREAD
        ).order_by('-created_at')
        
        page = self.paginate_queryset(unread_notifications)
        if page is not None:
            serializer = NotificationSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = NotificationSimpleSerializer(unread_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读通知数量"""
        user = request.user
        count = NotificationService.get_user_unread_count(user.id)
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """标记通知为已读"""
        notification = self.get_object()
        
        if notification.recipient != request.user:
            return Response(
                {'error': '只能标记自己的通知为已读'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        success = NotificationService.mark_notification_as_read(
            str(notification.id), request.user.id
        )
        
        if success:
            return Response({'message': '通知已标记为已读'})
        else:
            return Response(
                {'error': '标记失败'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """标记所有通知为已读"""
        user = request.user
        
        updated_count = Notification.objects.filter(
            recipient=user,
            status=Notification.NotificationStatus.UNREAD
        ).update(status=Notification.NotificationStatus.READ)
        
        return Response({
            'message': f'已标记 {updated_count} 条通知为已读'
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取通知统计信息"""
        user = request.user
        
        # 总通知数
        total_notifications = Notification.objects.filter(recipient=user).count()
        
        # 未读通知数
        unread_notifications = Notification.objects.filter(
            recipient=user,
            status=Notification.NotificationStatus.UNREAD
        ).count()
        
        # 按类型统计
        notifications_by_type = {}
        type_stats = Notification.objects.filter(recipient=user).values(
            'notification_type'
        ).annotate(count=Count('id'))
        
        for stat in type_stats:
            type_name = dict(Notification.NotificationType.choices).get(
                stat['notification_type'], stat['notification_type']
            )
            notifications_by_type[stat['notification_type']] = {
                'name': type_name,
                'count': stat['count']
            }
        
        # 按渠道统计（这里简化处理）
        notifications_by_channel = {
            'system': total_notifications,  # 所有通知都有系统内通知
            'email': 0,
            'sms': 0,
            'shihuatong': 0
        }
        
        # 最近通知
        recent_notifications = Notification.objects.filter(
            recipient=user
        ).order_by('-created_at')[:10]
        
        stats_data = {
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'notifications_by_type': notifications_by_type,
            'notifications_by_channel': notifications_by_channel,
            'recent_notifications': recent_notifications
        }
        
        serializer = NotificationStatsSerializer(stats_data)
        return Response(serializer.data)


class NotificationTemplateViewSet(ModelViewSet):
    """通知模板管理视图集"""
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['notification_type', 'status']
    search_fields = ['name', 'title_template', 'content_template']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class NotificationLogViewSet(ModelViewSet):
    """通知发送日志视图集"""
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['channel', 'status', 'notification__recipient']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    http_method_names = ['get']  # 只允许查看
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return NotificationLog.objects.all()
        else:
            # 普通用户只能看到自己的通知日志
            return NotificationLog.objects.filter(
                notification__recipient=user
            )


class UserNotificationSettingsViewSet(ModelViewSet):
    """用户通知设置视图集"""
    queryset = UserNotificationSettings.objects.all()
    serializer_class = UserNotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']  # 不允许创建和删除
    
    def get_queryset(self):
        """用户只能访问自己的设置"""
        return UserNotificationSettings.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_settings(self, request):
        """获取当前用户的通知设置"""
        settings, created = UserNotificationSettings.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_my_settings(self, request):
        """更新当前用户的通知设置"""
        settings, created = UserNotificationSettings.objects.get_or_create(
            user=request.user
        )
        
        serializer = self.get_serializer(
            settings, 
            data=request.data, 
            partial=request.method == 'PATCH'
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
