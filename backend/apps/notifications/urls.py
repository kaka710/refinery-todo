"""
通知相关URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationViewSet, NotificationTemplateViewSet,
    NotificationLogViewSet, UserNotificationSettingsViewSet
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'templates', NotificationTemplateViewSet)
router.register(r'logs', NotificationLogViewSet)
router.register(r'settings', UserNotificationSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
