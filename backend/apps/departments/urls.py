"""
部门相关URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, ProfessionViewSet, DepartmentCollaborationViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'professions', ProfessionViewSet)
router.register(r'collaborations', DepartmentCollaborationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
