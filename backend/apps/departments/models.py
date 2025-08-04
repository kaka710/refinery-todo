"""
部门模型
支持层级部门结构和专业分类
"""
from django.db import models
from django.core.validators import RegexValidator


class Department(models.Model):
    """
    部门模型
    支持树形结构的部门层级
    """
    class DepartmentType(models.TextChoices):
        COMPANY = 'company', '公司'
        DIVISION = 'division', '事业部'
        DEPARTMENT = 'department', '部门'
        SECTION = 'section', '科室'
        TEAM = 'team', '班组'
    
    class DepartmentStatus(models.TextChoices):
        ACTIVE = 'active', '正常'
        INACTIVE = 'inactive', '停用'
    
    # 基本信息
    name = models.CharField(max_length=100, verbose_name='部门名称')
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='部门编码',
        validators=[RegexValidator(r'^[A-Za-z0-9_-]+$', '部门编码只能包含字母、数字、下划线和横线')]
    )
    description = models.TextField(blank=True, verbose_name='部门描述')
    
    # 层级关系
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级部门'
    )
    level = models.PositiveIntegerField(default=0, verbose_name='层级')
    
    # 部门属性
    type = models.CharField(
        max_length=20,
        choices=DepartmentType.choices,
        default=DepartmentType.DEPARTMENT,
        verbose_name='部门类型'
    )
    status = models.CharField(
        max_length=20,
        choices=DepartmentStatus.choices,
        default=DepartmentStatus.ACTIVE,
        verbose_name='部门状态'
    )
    
    # 负责人 - 暂时注释掉避免循环依赖
    # manager = models.ForeignKey(
    #     'users.User',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='managed_departments',
    #     verbose_name='部门负责人'
    # )
    
    # 联系信息
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=200, blank=True, verbose_name='办公地址')
    
    # 排序
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'departments'
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['level', 'sort_order', 'name']
        unique_together = [['parent', 'name']]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """保存时自动计算层级"""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """获取完整部门路径"""
        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name
    
    def get_ancestors(self):
        """获取所有上级部门"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self):
        """获取所有下级部门"""
        descendants = []
        
        def collect_children(dept):
            for child in dept.children.filter(status=self.DepartmentStatus.ACTIVE):
                descendants.append(child)
                collect_children(child)
        
        collect_children(self)
        return descendants
    
    def get_all_users(self):
        """获取部门及其下级部门的所有用户"""
        from apps.users.models import User
        department_ids = [self.id] + [dept.id for dept in self.get_descendants()]
        return User.objects.filter(department_id__in=department_ids, status=User.UserStatus.ACTIVE)


class Profession(models.Model):
    """
    专业分类模型
    用于任务的专业分类管理
    """
    class ProfessionStatus(models.TextChoices):
        ACTIVE = 'active', '正常'
        INACTIVE = 'inactive', '停用'
    
    # 基本信息
    name = models.CharField(max_length=100, verbose_name='专业名称')
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='专业编码',
        validators=[RegexValidator(r'^[A-Za-z0-9_-]+$', '专业编码只能包含字母、数字、下划线和横线')]
    )
    description = models.TextField(blank=True, verbose_name='专业描述')
    
    # 所属部门
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='professions',
        verbose_name='所属部门'
    )
    
    # 专业负责人 - 暂时注释掉避免循环依赖
    # manager = models.ForeignKey(
    #     'users.User',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='managed_professions',
    #     verbose_name='专业负责人'
    # )
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=ProfessionStatus.choices,
        default=ProfessionStatus.ACTIVE,
        verbose_name='专业状态'
    )
    
    # 排序
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'professions'
        verbose_name = '专业'
        verbose_name_plural = '专业'
        ordering = ['department', 'sort_order', 'name']
        unique_together = [['department', 'name']]
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"
    
    def get_users(self):
        """获取专业相关用户"""
        from apps.users.models import User
        # 获取专业负责人和部门内的执行人
        users = User.objects.filter(
            department=self.department,
            status=User.UserStatus.ACTIVE
        )
        return users


class DepartmentCollaboration(models.Model):
    """
    部门协作关系模型
    用于记录跨部门协作的固定关系
    """
    class CollaborationType(models.TextChoices):
        REGULAR = 'regular', '常规协作'
        STRATEGIC = 'strategic', '战略协作'
        PROJECT = 'project', '项目协作'
    
    # 协作部门
    primary_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='primary_collaborations',
        verbose_name='主导部门'
    )
    secondary_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='secondary_collaborations',
        verbose_name='协作部门'
    )
    
    # 协作信息
    collaboration_type = models.CharField(
        max_length=20,
        choices=CollaborationType.choices,
        default=CollaborationType.REGULAR,
        verbose_name='协作类型'
    )
    description = models.TextField(blank=True, verbose_name='协作描述')
    
    # 是否激活
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'department_collaborations'
        verbose_name = '部门协作关系'
        verbose_name_plural = '部门协作关系'
        unique_together = [['primary_department', 'secondary_department']]
    
    def __str__(self):
        return f"{self.primary_department.name} <-> {self.secondary_department.name}"
