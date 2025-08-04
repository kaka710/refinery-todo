#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南炼化Todo系统 - GitHub上传工具
自动化上传项目到GitHub仓库
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class GitHubUploader:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.git_path = self.find_git()
        
    def find_git(self):
        """查找Git可执行文件"""
        possible_paths = [
            "git",  # 系统PATH中
            "D:\\Tools\\Git\\bin\\git.exe",  # 用户指定路径
            "C:\\Program Files\\Git\\bin\\git.exe",  # 默认安装路径
            "C:\\Program Files (x86)\\Git\\bin\\git.exe"
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ 找到Git: {path}")
                    print(f"   版本: {result.stdout.strip()}")
                    return path
            except:
                continue
        
        print("❌ 未找到Git，请先安装Git")
        return None
    
    def run_git_command(self, command, check=True):
        """执行Git命令"""
        if not self.git_path:
            print("❌ Git不可用")
            return False
            
        try:
            full_command = [self.git_path] + command
            print(f"🔧 执行: {' '.join(full_command)}")
            
            result = subprocess.run(full_command, 
                                  cwd=self.project_dir,
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)
            
            if result.stdout:
                print(f"📤 输出: {result.stdout.strip()}")
            if result.stderr and result.returncode != 0:
                print(f"⚠️  错误: {result.stderr.strip()}")
                
            if check and result.returncode != 0:
                return False
            return True
            
        except subprocess.TimeoutExpired:
            print("⏰ 命令执行超时")
            return False
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 敏感信息
*.key
*.pem
.env
.env.local
.env.production
config/secrets.py

# 临时文件
*.tmp
*.temp
*.bak
*.backup

# 日志文件
logs/
*.log

# 缓存
.cache/
.pytest_cache/
"""
        
        gitignore_path = self.project_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ 创建 .gitignore 文件")
    
    def create_readme(self):
        """创建README.md文件"""
        readme_content = """# 🏭 海南炼化Todo系统

## 📋 项目简介

海南炼化Todo系统是一个专为石化企业设计的任务管理系统，集成了石化通(Shihuatong)平台，支持多级权限管理和部门协作。

## ✨ 主要功能

### 🔐 用户管理
- **多角色权限控制**: 系统管理员、部门负责人、专业负责人、执行人
- **部门组织架构**: 支持多部门用户管理
- **用户信息管理**: 完整的用户档案和权限配置

### 📝 任务管理
- **任务创建**: 支持一对一和一对多分配模式
- **任务跟踪**: 实时任务状态更新和进度监控
- **协作功能**: 跨部门任务协作和人员配置
- **优先级管理**: 任务优先级设置和紧急任务处理

### 📊 数据统计
- **人员统计**: 各部门人员数量和角色分布
- **任务统计**: 任务完成情况和效率分析
- **部门统计**: 部门工作负载和绩效指标

## 🛠️ 技术栈

### 后端技术
- **Django 4.2**: Web框架
- **Django REST Framework**: API开发
- **MySQL**: 数据库
- **JWT**: 身份认证
- **Gunicorn**: WSGI服务器

### 前端技术
- **Vue 3**: 前端框架
- **Element Plus**: UI组件库
- **Vite**: 构建工具
- **Axios**: HTTP客户端

### 部署技术
- **Docker**: 容器化部署
- **Nginx**: 反向代理
- **HTTPS**: 安全传输

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/hainan-refinery-todo.git
cd hainan-refinery-todo
```

2. **启动系统**
```bash
# Windows用户
launcher.bat

# 或者使用Python脚本
python 简单启动.py
```

3. **访问系统**
- 前端地址: https://127.0.0.1:5173
- 后端API: https://127.0.0.1:8000

### 默认账户
- **管理员**: admin / admin123
- **部门负责人**: zhangsan / password123
- **专业负责人**: lisi / password123
- **执行人**: zhaoliu / password123

## 📁 项目结构

```
海南炼化Todo系统/
├── backend/                 # Django后端
│   ├── apps/               # 应用模块
│   ├── todo_system/        # 项目配置
│   ├── requirements.txt    # Python依赖
│   └── manage.py          # Django管理脚本
├── frontend/               # Vue前端
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   ├── package.json       # Node.js依赖
│   └── vite.config.js     # Vite配置
├── ssl/                   # SSL证书
├── docker-compose.yml     # Docker配置
├── launcher.bat          # Windows启动脚本
└── 简单启动.py           # Python启动脚本
```

## 🔧 配置说明

### 数据库配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'todo_db',
        'USER': 'root',
        'PASSWORD': 'hnlh1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### HTTPS配置
系统强制使用HTTPS，SSL证书位于 `ssl/` 目录。

## 📖 使用文档

详细的使用说明请参考项目中的文档文件：
- `使用说明.txt` - 基本使用指南
- `用户清单和密码.md` - 用户账户信息
- 各种修复说明文档 - 技术问题解决方案

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues](https://github.com/your-username/hainan-refinery-todo/issues)
- 邮箱: your-email@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---
**海南炼化Todo系统** - 让任务管理更高效 🚀
"""
        
        readme_path = self.project_dir / "README_GitHub.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ 创建 README_GitHub.md 文件")
    
    def init_git_repo(self):
        """初始化Git仓库"""
        print("\n🔧 初始化Git仓库...")
        
        # 检查是否已经是Git仓库
        if (self.project_dir / ".git").exists():
            print("✅ Git仓库已存在")
            return True
        
        # 初始化仓库
        if not self.run_git_command(["init"]):
            return False
        
        # 配置用户信息（如果未配置）
        self.run_git_command(["config", "user.name", "海南炼化开发团队"], check=False)
        self.run_git_command(["config", "user.email", "dev@hainan-refinery.com"], check=False)
        
        return True
    
    def add_and_commit(self):
        """添加文件并提交"""
        print("\n📦 添加文件到Git...")
        
        # 添加所有文件
        if not self.run_git_command(["add", "."]):
            return False
        
        # 检查状态
        self.run_git_command(["status"], check=False)
        
        # 提交
        commit_message = "feat: 海南炼化Todo系统初始版本\n\n- 完整的任务管理功能\n- 多角色权限控制\n- 部门协作支持\n- HTTPS安全配置\n- Docker容器化部署"
        
        if not self.run_git_command(["commit", "-m", commit_message]):
            print("⚠️  可能没有文件需要提交")
        
        return True
    
    def show_github_instructions(self):
        """显示GitHub操作指南"""
        print("\n" + "="*60)
        print("🎯 GitHub仓库创建和上传指南")
        print("="*60)
        
        print("\n📋 步骤1: 在GitHub上创建仓库")
        print("1. 访问 https://github.com")
        print("2. 点击右上角的 '+' 按钮，选择 'New repository'")
        print("3. 填写仓库信息:")
        print("   - Repository name: hainan-refinery-todo")
        print("   - Description: 海南炼化Todo任务管理系统")
        print("   - 选择 Public 或 Private")
        print("   - 不要勾选 'Initialize this repository with a README'")
        print("4. 点击 'Create repository'")
        
        print("\n📋 步骤2: 复制仓库URL")
        print("创建仓库后，复制仓库的HTTPS URL，格式如:")
        print("https://github.com/your-username/hainan-refinery-todo.git")
        
        print("\n📋 步骤3: 执行上传命令")
        print("在当前目录执行以下命令:")
        print(f"cd \"{self.project_dir}\"")
        print("git remote add origin https://github.com/your-username/hainan-refinery-todo.git")
        print("git branch -M main")
        print("git push -u origin main")
        
        print("\n📋 步骤4: 输入GitHub凭据")
        print("- Username: 你的GitHub用户名")
        print("- Password: 你的GitHub Personal Access Token")
        print("  (不是密码，需要在GitHub Settings > Developer settings > Personal access tokens 中创建)")
        
        print("\n✅ 完成后，你的项目就会出现在GitHub上！")
        print("="*60)
    
    def run(self):
        """运行上传流程"""
        print("🚀 海南炼化Todo系统 - GitHub上传工具")
        print("="*50)
        
        if not self.git_path:
            return False
        
        # 创建必要文件
        self.create_gitignore()
        self.create_readme()
        
        # 初始化Git仓库
        if not self.init_git_repo():
            print("❌ Git仓库初始化失败")
            return False
        
        # 添加和提交文件
        if not self.add_and_commit():
            print("❌ 文件提交失败")
            return False
        
        # 显示GitHub操作指南
        self.show_github_instructions()
        
        print("\n🎉 本地Git仓库准备完成！")
        print("请按照上面的指南在GitHub上创建仓库并上传代码。")
        
        return True

if __name__ == "__main__":
    uploader = GitHubUploader()
    success = uploader.run()
    
    if success:
        print("\n✅ 准备工作完成！")
    else:
        print("\n❌ 准备工作失败！")
    
    input("\n按回车键退出...")
