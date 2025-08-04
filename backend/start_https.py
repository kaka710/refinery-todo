#!/usr/bin/env python
"""
使用Waitress启动支持HTTPS的Django服务
"""
import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_system.settings')

# 获取WSGI应用
application = get_wsgi_application()

if __name__ == "__main__":
    # 使用Waitress启动HTTPS服务器
    print("Starting HTTPS server on https://0.0.0.0:8000")
    print("Using SSL certificate: ../ssl/cert.pem")
    print("Using SSL key: ../ssl/key.pem")
    print("Quit the server with CTRL-BREAK.")
    
    # 启动服务器
    serve(
        application,
        host='0.0.0.0',
        port=8000,
        certfile='../ssl/cert.pem',
        keyfile='../ssl/key.pem'
    )