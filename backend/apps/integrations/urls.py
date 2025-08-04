"""
集成相关URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShihuatongIntegrationViewSet, ShihuatongMessageViewSet,
    ShihuatongUserMappingViewSet, IntegrationLogViewSet
)

router = DefaultRouter()
router.register(r'shihuatong/integrations', ShihuatongIntegrationViewSet)
router.register(r'shihuatong/messages', ShihuatongMessageViewSet)
router.register(r'shihuatong/mappings', ShihuatongUserMappingViewSet)
router.register(r'logs', IntegrationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
