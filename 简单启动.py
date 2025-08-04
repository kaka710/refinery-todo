#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南炼化Todo系统简单启动脚本
直接在当前目录执行，避免路径问题
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("           🏭 海南炼化Todo系统简单启动器")
    print("=" * 60)
    print("版本: 简化版")
    print("描述: 企业级任务管理系统")
    print("=" * 60)
    print()

def check_environment():
    """检查基本环境"""
    print("🔍 检查环境...")
    
    # 检查Python
    version = sys.version_info
    print(f"✅ Python: {version.major}.{version.minor}.{version.micro}")
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"✅ 当前目录: {current_dir}")
    
    # 检查关键文件
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir / "frontend"
    
    if backend_dir.exists():
        print("✅ backend目录存在")
    else:
        print("❌ backend目录不存在")
        return False
    
    if frontend_dir.exists():
        print("✅ frontend目录存在")
    else:
        print("❌ frontend目录不存在")
        return False
    
    return True

def select_mode():
    """选择启动模式"""
    print("\n🚀 选择启动模式:")
    print("1. 快速启动 (SQLite)")
    print("2. 完整启动 (MySQL)")
    print("3. 仅启动后端")
    print("4. 仅启动前端")
    
    while True:
        try:
            choice = input("请选择 (1-4) [默认: 1]: ").strip()
            if not choice:
                choice = "1"
            
            if choice in ["1", "2", "3", "4"]:
                return choice
            else:
                print("❌ 请输入 1-4")
        except KeyboardInterrupt:
            print("\n❌ 用户取消")
            sys.exit(1)

def start_backend(use_mysql=False):
    """启动后端服务"""
    print("\n🚀 启动后端服务...")
    
    try:
        backend_dir = Path.cwd() / "backend"
        os.chdir(backend_dir)
        
        if use_mysql:
            cmd = [sys.executable, "manage.py", "runserver", "127.0.0.1:8000", "--settings=simple_settings"]
        else:
            cmd = [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"]
        
        # 在新窗口启动后端
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k'] + [' '.join(cmd)])
        else:
            subprocess.Popen(cmd)
        
        print("✅ 后端服务启动中...")
        return True
        
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        return False
    finally:
        os.chdir(Path.cwd().parent)

def start_frontend():
    """启动前端服务"""
    print("\n🚀 启动前端服务...")
    
    try:
        frontend_dir = Path.cwd() / "frontend"
        os.chdir(frontend_dir)
        
        cmd = ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"]
        
        # 在新窗口启动前端
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k'] + [' '.join(cmd)])
        else:
            subprocess.Popen(cmd)
        
        print("✅ 前端服务启动中...")
        return True
        
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return False
    finally:
        os.chdir(Path.cwd().parent)

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        input("\n按回车键退出...")
        return
    
    # 选择模式
    mode = select_mode()
    
    success = True
    
    if mode == "1":  # 快速启动 SQLite
        print("\n🚀 快速启动模式 (SQLite)")
        success &= start_backend(use_mysql=False)
        time.sleep(2)
        success &= start_frontend()
        
    elif mode == "2":  # 完整启动 MySQL
        print("\n🚀 完整启动模式 (MySQL)")
        success &= start_backend(use_mysql=True)
        time.sleep(2)
        success &= start_frontend()
        
    elif mode == "3":  # 仅后端
        print("\n🚀 仅启动后端")
        use_mysql = input("使用MySQL? (y/N): ").strip().lower() == 'y'
        success &= start_backend(use_mysql=use_mysql)
        
    elif mode == "4":  # 仅前端
        print("\n🚀 仅启动前端")
        success &= start_frontend()
    
    if success:
        print("\n" + "=" * 60)
        print("                    🎉 启动完成！")
        print("=" * 60)
        print("\n🌐 访问地址：")
        if mode in ["1", "2"]:
            print("   前端界面: http://127.0.0.1:5173/")
            print("   后端API:  http://127.0.0.1:8000/")
        elif mode == "3":
            print("   后端API:  http://127.0.0.1:8000/")
        elif mode == "4":
            print("   前端界面: http://127.0.0.1:5173/")
        
        print("\n💡 默认账号: admin / admin123")
        print("💡 关闭服务窗口即可停止服务")
    else:
        print("\n❌ 启动过程中出现错误")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断启动")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        input("按回车键退出...")
