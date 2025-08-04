"""
用户相关URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView, LogoutView, UserViewSet, UserRegistrationView, UserLoginLogViewSet,
    UserPermissionsView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'login-logs', UserLoginLogViewSet)

urlpatterns = [
    # 认证相关
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('permissions/', UserPermissionsView.as_view(), name='user_permissions'),

    # 用户管理
    path('', include(router.urls)),
]
