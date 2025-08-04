"""
任务相关URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet, TaskAssignmentViewSet, TaskExecutionViewSet,
    TaskReviewViewSet, TaskAttachmentViewSet, TaskCommentViewSet,
    TaskTemplateViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'assignments', TaskAssignmentViewSet)
router.register(r'executions', TaskExecutionViewSet)
router.register(r'reviews', TaskReviewViewSet)
router.register(r'attachments', TaskAttachmentViewSet)
router.register(r'comments', TaskCommentViewSet)
router.register(r'templates', TaskTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
