#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 如果使用runsslserver命令且没有指定证书路径，则使用项目根目录下的ssl证书
    if 'runsslserver' in sys.argv and '--certificate' not in sys.argv and '--key' not in sys.argv:
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 证书文件路径
        cert_file = os.path.join(project_root, 'ssl', 'cert.pem')
        key_file = os.path.join(project_root, 'ssl', 'key.pem')
        
        # 添加证书参数
        if os.path.exists(cert_file) and os.path.exists(key_file):
            sys.argv.extend(['--certificate', cert_file, '--key', key_file])
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
