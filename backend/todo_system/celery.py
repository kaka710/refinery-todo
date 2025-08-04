"""
Celery配置文件
用于异步任务处理，特别是石化通消息推送
"""
import os
from celery import Celery

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_system.settings')

app = Celery('todo_system')

# 使用Django设置配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
