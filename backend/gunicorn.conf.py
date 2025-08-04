# Gunicorn配置文件
# 用于启动支持HTTPS的Django服务

# 绑定地址和端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = 2

# 工作进程类型
worker_class = "gevent"

# SSL证书和密钥文件路径
certfile = "../ssl/cert.pem"
keyfile = "../ssl/key.pem"

# 日志级别
loglevel = "info"

# 访问日志和错误日志
accesslog = "-"
errorlog = "-"

# 启用后台运行
daemon = False

# 进程名
proc_name = "todo_backend"

# 超时设置
timeout = 30

# 优雅关闭超时
graceful_timeout = 30

# 预加载应用
preload_app = True