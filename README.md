# 海南炼化Todo系统 - 生产环境

🔒 **企业级任务管理系统 - 仅支持HTTPS安全访问**

基于Django + Vue.js的企业级任务管理系统，集成石化通消息推送服务，专为生产环境设计。

## 🚀 生产环境快速启动

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+ (推荐生产环境)
- Redis 6.0+ (用于缓存和Celery任务队列)

### 一键启动

**方法1：双击启动（推荐）**
```
双击运行: start.bat
```

**方法2：Python启动**
```bash
python start.py
```

**方法3：Docker启动**
```bash
docker-compose up -d
```

**方法4：手动启动**
```bash
# 1. 启动后端
cd backend
python manage.py runserver 127.0.0.1:8000

# 2. 启动前端（新终端窗口）
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

### 访问地址 (仅HTTPS)

🔒 **系统已配置为生产环境，仅支持HTTPS访问：**

- 📱 **前端界面**: https://127.0.0.1:5173/
- 🔧 **后端API**: https://127.0.0.1:8000/
- 📚 **API文档**: https://127.0.0.1:8000/api/docs/

⚠️ **重要提示**: 所有HTTP请求将自动重定向到HTTPS

## 🔒 安全特性

### 生产环境安全配置
- ✅ **强制HTTPS**: 禁用所有HTTP访问
- ✅ **DEBUG禁用**: 生产环境禁用调试模式
- ✅ **SSL/TLS加密**: 自动生成和配置SSL证书
- ✅ **安全HTTP头**: HSTS、CSP、XSS保护等
- ✅ **Cookie安全**: 强制安全Cookie设置
- ✅ **CSRF保护**: 跨站请求伪造防护

### 数据安全
- ✅ **加密传输**: 所有数据通过HTTPS加密传输
- ✅ **JWT认证**: 安全的用户身份验证
- ✅ **权限控制**: 基于角色的访问控制
- ✅ **数据验证**: 严格的输入验证和过滤

## 📁 生产环境项目结构

```
海南炼化Todo系统/
├── start.bat              # 一键启动脚本
├── start.py               # Python启动器
├── README.md              # 项目文档
├── backend/               # Django后端
│   ├── apps/             # 应用模块
│   │   ├── users/        # 用户管理
│   │   ├── tasks/        # 任务管理
│   │   ├── notifications/# 通知系统
│   │   └── integrations/ # 石化通集成
│   ├── todo_system/      # 项目配置
│   ├── start_https.py    # HTTPS服务启动脚本
│   ├── manage.py         # Django管理脚本
│   └── requirements.txt  # Python依赖
├── frontend/             # Vue.js前端
│   ├── src/             # 源代码
│   ├── public/          # 静态资源
│   ├── package.json     # Node.js依赖
│   └── vite.config.js   # Vite配置
├── ssl/                 # SSL证书目录
│   ├── cert.pem        # SSL证书
│   └── key.pem         # SSL私钥
├── generate_cert.py    # SSL证书生成脚本
├── docker-compose.yml  # Docker配置
└── 标准文件/           # 石化通集成文档
```

## 🔧 核心功能

### 任务管理
- ✅ 任务创建、分配、跟踪
- ✅ 任务状态管理和流程控制
- ✅ 任务优先级和截止日期
- ✅ 任务评论和协作

### 用户管理
- ✅ 四级权限体系 (系统管理员/部门负责人/专业负责人/执行人)
- ✅ 用户认证与授权
- ✅ 用户资料管理
- ✅ 登录日志记录

### 通知系统
- ✅ 实时消息通知
- ✅ 邮件通知
- ✅ 石化通集成推送
- ✅ 系统公告

### 数据统计
- ✅ 任务完成率统计
- ✅ 用户工作量分析
- ✅ 部门绩效报表
- ✅ 数据可视化图表

## 🔗 石化通集成

系统深度集成中国石化石化通消息推送服务：

### 集成功能
- ✅ 任务状态变更自动通知
- ✅ 重要事件实时提醒
- ✅ 系统消息推送
- ✅ AES加密数据传输

### 配置方法
在 `backend/.env` 文件中配置：
```env
# 石化通集成配置
SHT_WEBHOOK_URL=https://t01.gws.jtsh.icloud.sinopec.com/IMPushApi/api/WebhookIMPush/Create
SHT_APP_CODE=your-app-code
SHT_AES_KEY=your-aes-key
SHT_AES_IV=your-aes-iv
SHT_APP_KEY=your-app-key
SHT_APP_SECRET=your-app-secret
```

## 🐳 Docker生产部署

### 快速部署
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 服务组件
- **todo_backend**: Django后端服务 (HTTPS)
- **todo_frontend**: Vue.js前端服务 (HTTPS)
- **mysql**: MySQL数据库
- **redis**: Redis缓存和消息队列

## 📊 技术架构

### 后端技术栈 (生产优化)
- **框架**: Django 4.2 (生产模式)
- **WSGI服务器**: Gunicorn + Waitress (HTTPS)
- **API**: Django REST Framework
- **数据库**: MySQL 8.0 (生产推荐)
- **缓存**: Redis 6.0
- **任务队列**: Celery
- **认证**: JWT (安全配置)

### 前端技术栈 (生产构建)
- **框架**: Vue.js 3 (生产构建)
- **构建工具**: Vite (优化构建)
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router (HTTPS模式)

## 🛠️ 生产环境管理

### 服务管理
```cmd
# 检查服务状态
check_services.bat

# 重新生成SSL证书
python generate_cert.py

# 查看系统日志
# 日志位置: backend/logs/
```

### 数据库管理
```bash
# 数据库迁移
cd backend
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic
```

### 性能监控
- 系统资源监控
- 数据库性能监控
- API响应时间监控
- 用户访问日志分析

## 🔍 故障排除

### SSL证书问题
```cmd
# 重新生成SSL证书
python generate_cert.py

# 检查证书有效性
openssl x509 -in ssl/cert.pem -text -noout
```

### 服务启动问题
```cmd
# 检查端口占用
netstat -an | findstr ":8000"
netstat -an | findstr ":5173"

# 检查防火墙设置
# 确保允许HTTPS端口 (443, 8000, 5173)
```

### 数据库连接问题
1. 检查MySQL服务状态
2. 验证数据库配置 (.env文件)
3. 确认网络连接
4. 检查用户权限

## 📋 用户角色权限

| 角色 | 权限范围 | 主要功能 |
|------|----------|----------|
| **系统管理员** | 全系统 | 用户管理、系统配置、数据统计 |
| **部门负责人** | 本部门 | 部门任务管理、人员分配 |
| **专业负责人** | 专业领域 | 专业任务管理、技术指导 |
| **执行人** | 个人任务 | 任务执行、状态更新、反馈 |

## 📞 技术支持

### 联系方式
- **技术支持**: 海南炼化IT部门
- **系统管理**: 系统管理员
- **使用培训**: 各部门负责人

### 文档资源
- 📚 **API文档**: https://127.0.0.1:8000/api/docs/
- 📖 **用户手册**: 系统内置帮助
- 🔧 **管理指南**: 管理员后台

## 📄 版权声明

**海南炼化Todo系统** - 企业内部专用系统

- 版权所有 © 海南炼化
- 仅限企业内部使用
- 禁止未授权复制或分发
- 技术支持：海南炼化IT部门

---

🔒 **安全提醒**: 本系统已配置为生产环境，请确保：
1. 定期更新SSL证书
2. 监控系统安全日志
3. 及时安装安全更新
4. 遵循企业安全规范
