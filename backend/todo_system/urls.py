"""
海南炼化Todo系统 URL配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_info(request):
    """API信息页面"""
    return JsonResponse({
        'message': '海南炼化Todo系统 API服务',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'api_docs': '/api/docs/',
            'api_redoc': '/api/redoc/',
            'admin': '/admin/',
            'auth': '/api/v1/auth/',
            'departments': '/api/v1/departments/',
            'tasks': '/api/v1/tasks/',
            'notifications': '/api/v1/notifications/',
            'integrations': '/api/v1/integrations/',
        },
        'frontend_url': 'http://127.0.0.1:5173/',
        'note': '这是后端API服务，请访问前端界面: http://127.0.0.1:5173/'
    })

urlpatterns = [
    # 根路径 - API信息
    path('', api_info, name='api_info'),

    # 管理后台
    path('admin/', admin.site.urls),

    # API文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API路由
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/departments/', include('apps.departments.urls')),
    path('api/v1/tasks/', include('apps.tasks.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/integrations/', include('apps.integrations.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
