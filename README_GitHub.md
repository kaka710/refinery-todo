# 🏭 海南炼化Todo系统

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
