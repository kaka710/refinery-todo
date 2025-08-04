"""
用户相关视图
"""
import logging
from django.contrib.auth import login
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, UserProfile, UserLoginLog
from .serializers import (
    UserSerializer, UserSimpleSerializer, LoginSerializer, TokenSerializer,
    ChangePasswordSerializer, UserRegistrationSerializer, UserLoginLogSerializer,
    UserPermissionSerializer, UserProfileSerializer
)
from .permissions import IsAdminOrSelf, IsAdminUser

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 记录登录日志
            self._log_login_attempt(request, user, True)
            
            # 更新最后登录信息
            user.last_login = timezone.now()
            user.last_login_ip = self._get_client_ip(request)
            user.save(update_fields=['last_login', 'last_login_ip'])
            
            # 生成JWT Token
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        # 记录失败的登录尝试
        self._log_login_attempt(request, None, False, serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _log_login_attempt(self, request, user, is_success, failure_reason=None):
        """记录登录尝试"""
        try:
            UserLoginLog.objects.create(
                user=user,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                is_success=is_success,
                failure_reason=str(failure_reason) if failure_reason else ''
            )
        except Exception as e:
            logger.error(f"记录登录日志失败: {e}")


class LogoutView(APIView):
    """用户登出视图"""
    permission_classes = [permissions.AllowAny]  # 允许任何人调用登出
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as token_error:
                    # 如果token blacklist失败，记录日志但不阻止登出
                    logger.warning(f"Token blacklist失败: {token_error}")

            return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"登出失败: {e}")
            # 即使出错也返回成功，因为前端需要清理本地状态
            return Response({'message': '登出成功'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'status', 'department']
    search_fields = ['username', 'real_name', 'employee_id', 'email']
    ordering_fields = ['created_at', 'last_login', 'real_name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """根据操作类型设置权限"""
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrSelf]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == 'list':
            return UserSimpleSerializer
        return UserSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return User.objects.all()
        elif user.is_dept_manager and user.department:
            # 部门负责人只能看到自己部门的用户
            return User.objects.filter(department=user.department)
        else:
            # 普通用户只能看到自己
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """更新用户资料"""
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """修改密码"""
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': '密码修改成功'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def permissions(self, request):
        """获取用户权限信息"""
        serializer = UserPermissionSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活用户"""
        if not request.user.is_admin:
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        user.status = User.UserStatus.ACTIVE
        user.is_active = True
        user.save(update_fields=['status', 'is_active'])
        
        return Response({'message': '用户已激活'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用用户"""
        if not request.user.is_admin:
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': '不能停用自己的账号'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.status = User.UserStatus.DISABLED
        user.is_active = False
        user.save(update_fields=['status', 'is_active'])
        
        return Response({'message': '用户已停用'})


class UserRegistrationView(APIView):
    """用户注册视图"""
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # 返回创建的用户信息
            response_serializer = UserSerializer(user)
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginLogViewSet(ModelViewSet):
    """用户登录日志视图集"""
    queryset = UserLoginLog.objects.all()
    serializer_class = UserLoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_success', 'user']
    search_fields = ['user__real_name', 'ip_address']
    ordering_fields = ['login_time']
    ordering = ['-login_time']
    http_method_names = ['get']  # 只允许查看
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user
        
        if user.is_admin:
            return UserLoginLog.objects.all()
        else:
            # 普通用户只能看到自己的登录日志
            return UserLoginLog.objects.filter(user=user)


class UserPermissionsView(APIView):
    """用户权限信息视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取当前用户权限信息"""
        user = request.user
        is_admin = getattr(user, 'role', 'user') == 'admin' or user.is_superuser
        permissions_data = {
            'user_id': user.id,
            'username': user.username,
            'role': getattr(user, 'role', 'user'),
            'is_superuser': user.is_superuser,
            'permissions': {
                'can_create_task': True,
                'can_edit_task': True,
                'can_delete_task': is_admin or user.role in ['admin', 'dept_manager'],
                'can_manage_users': is_admin,
                'can_view_reports': True,
                'is_admin': is_admin,
            },
            'managed_departments': []
        }
        return Response(permissions_data)
