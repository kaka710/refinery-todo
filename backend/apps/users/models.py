"""
用户模型
支持四种角色：系统管理员、部门负责人、专业负责人、执行人
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    自定义用户模型
    """
    class UserRole(models.TextChoices):
        ADMIN = 'admin', '系统管理员'
        DEPT_MANAGER = 'dept_manager', '部门负责人'
        PROF_MANAGER = 'prof_manager', '专业负责人'
        EXECUTOR = 'executor', '执行人'
    
    class UserStatus(models.TextChoices):
        ACTIVE = 'active', '激活'
        INACTIVE = 'inactive', '未激活'
        DISABLED = 'disabled', '禁用'
    
    # 基本信息
    employee_id = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='工号',
        validators=[RegexValidator(r'^[A-Za-z0-9]+$', '工号只能包含字母和数字')]
    )
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    phone = models.CharField(
        max_length=11, 
        blank=True, 
        verbose_name='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')]
    )
    
    # 角色和权限
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices, 
        default=UserRole.EXECUTOR,
        verbose_name='用户角色'
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        verbose_name='用户状态'
    )
    
    # 组织架构
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='所属部门'
    )
    
    # 石化通相关
    shihuatong_user_id = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='石化通用户ID'
    )
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='最后登录IP')
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.real_name}({self.employee_id})"
    
    @property
    def is_admin(self):
        """是否为系统管理员"""
        return self.role == self.UserRole.ADMIN
    
    @property
    def is_dept_manager(self):
        """是否为部门负责人"""
        return self.role == self.UserRole.DEPT_MANAGER
    
    @property
    def is_prof_manager(self):
        """是否为专业负责人"""
        return self.role == self.UserRole.PROF_MANAGER
    
    @property
    def is_executor(self):
        """是否为执行人"""
        return self.role == self.UserRole.EXECUTOR
    
    @property
    def can_create_task(self):
        """是否可以创建任务"""
        return self.role in [self.UserRole.ADMIN, self.UserRole.DEPT_MANAGER, self.UserRole.PROF_MANAGER]
    
    @property
    def can_manage_users(self):
        """是否可以管理用户"""
        return self.role == self.UserRole.ADMIN
    
    def get_managed_departments(self):
        """获取管理的部门"""
        if self.is_admin:
            from apps.departments.models import Department
            return Department.objects.all()
        elif self.is_dept_manager and self.department:
            return [self.department]
        return []


class UserProfile(models.Model):
    """
    用户扩展信息
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='用户'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='头像'
    )
    bio = models.TextField(blank=True, verbose_name='个人简介')
    
    # 通知设置
    email_notifications = models.BooleanField(default=True, verbose_name='邮件通知')
    sms_notifications = models.BooleanField(default=True, verbose_name='短信通知')
    shihuatong_notifications = models.BooleanField(default=True, verbose_name='石化通通知')
    
    # 工作信息
    position = models.CharField(max_length=100, blank=True, verbose_name='职位')
    office_location = models.CharField(max_length=200, blank=True, verbose_name='办公地点')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f"{self.user.real_name}的资料"


class UserLoginLog(models.Model):
    """
    用户登录日志
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='login_logs',
        verbose_name='用户'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='用户代理')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    is_success = models.BooleanField(default=True, verbose_name='是否成功')
    failure_reason = models.CharField(max_length=200, blank=True, verbose_name='失败原因')
    
    class Meta:
        db_table = 'user_login_logs'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        ordering = ['-login_time']
    
    def __str__(self):
        status = '成功' if self.is_success else '失败'
        return f"{self.user.real_name} - {self.login_time} - {status}"
