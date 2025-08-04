#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南炼化Todo系统启动脚本 (英文文件名版本)
"""

import os
import sys
from pathlib import Path

def main():
    """主函数"""
    try:
        # 获取当前脚本所在目录
        current_dir = Path(__file__).parent.absolute()
        
        # 切换到脚本目录
        os.chdir(current_dir)
        
        # 导入并运行主启动脚本
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_launcher", "简单启动.py")
        main_launcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_launcher)
        
        # 运行主函数
        main_launcher.main()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
