"""
海南炼化Todo系统 - 安全中间件
强制HTTPS访问和安全头设置
"""

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class ForceHTTPSMiddleware(MiddlewareMixin):
    """强制HTTPS中间件"""
    
    def process_request(self, request):
        """处理请求，强制重定向到HTTPS"""
        if not settings.DEBUG and getattr(settings, 'FORCE_HTTPS', False):
            # 检查是否已经是HTTPS
            if not request.is_secure():
                # 检查是否通过代理转发的HTTPS
                forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO')
                if forwarded_proto != 'https':
                    # 重定向到HTTPS
                    https_url = request.build_absolute_uri().replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(https_url)
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """安全HTTP头中间件"""
    
    def process_response(self, request, response):
        """添加安全HTTP头"""
        security_headers = getattr(settings, 'SECURITY_HEADERS', {})
        
        for header, value in security_headers.items():
            response[header] = value
        
        return response


class HostValidationMiddleware(MiddlewareMixin):
    """Host头验证中间件"""
    
    def process_request(self, request):
        """验证Host头，防止Host头攻击"""
        host = request.get_host().split(':')[0]
        allowed_hosts = settings.ALLOWED_HOSTS
        
        # 如果设置了ALLOWED_HOSTS且当前host不在允许列表中
        if allowed_hosts and '*' not in allowed_hosts and host not in allowed_hosts:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest('Invalid Host header')
        
        return None
