"""
任务模型
支持任务创建、分配、执行、反馈等完整流程
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    """
    任务主表
    """
    class TaskType(models.TextChoices):
        NORMAL = 'normal', '普通任务'
        URGENT = 'urgent', '紧急任务'
        IMPORTANT = 'important', '重要任务'
        ROUTINE = 'routine', '例行任务'
    
    class TaskStatus(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PENDING = 'pending', '待接收'
        ACCEPTED = 'accepted', '已接收'
        IN_PROGRESS = 'in_progress', '进行中'
        COMPLETED = 'completed', '已完成'
        REVIEWED = 'reviewed', '已评价'
        CANCELLED = 'cancelled', '已取消'
        OVERDUE = 'overdue', '已逾期'
    
    class AssignmentMode(models.TextChoices):
        ONE_TO_ONE = 'one_to_one', '一对一分配'
        ONE_TO_MANY = 'one_to_many', '一对多分配'
        CROSS_DEPARTMENT = 'cross_department', '跨部门协同'
    
    class Priority(models.TextChoices):
        LOW = 'low', '低'
        MEDIUM = 'medium', '中'
        HIGH = 'high', '高'
        CRITICAL = 'critical', '紧急'
    
    # 基本信息
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(verbose_name='任务描述')
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.NORMAL,
        verbose_name='任务类型'
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name='优先级'
    )
    
    # 创建者信息
    creator = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='创建者'
    )
    creator_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='创建部门'
    )
    profession = models.ForeignKey(
        'departments.Profession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='所属专业'
    )
    
    # 分配模式
    assignment_mode = models.CharField(
        max_length=20,
        choices=AssignmentMode.choices,
        default=AssignmentMode.ONE_TO_ONE,
        verbose_name='分配模式'
    )
    
    # 时间信息
    start_date = models.DateTimeField(verbose_name='开始时间')
    due_date = models.DateTimeField(verbose_name='截止时间')
    estimated_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='预估工时(小时)'
    )
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.DRAFT,
        verbose_name='任务状态'
    )
    
    # 附件
    has_attachments = models.BooleanField(default=False, verbose_name='是否有附件')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        db_table = 'tasks'
        verbose_name = '任务'
        verbose_name_plural = '任务'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['creator', 'status']),
            models.Index(fields=['creator_department', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """是否已逾期"""
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status not in [
            self.TaskStatus.COMPLETED, 
            self.TaskStatus.REVIEWED, 
            self.TaskStatus.CANCELLED
        ]
    
    @property
    def progress_percentage(self):
        """任务进度百分比"""
        if self.status == self.TaskStatus.COMPLETED:
            return 100
        elif self.status == self.TaskStatus.IN_PROGRESS:
            # 根据子任务完成情况计算
            assignments = self.assignments.all()
            if assignments:
                completed_count = assignments.filter(status=TaskAssignment.AssignmentStatus.COMPLETED).count()
                return int((completed_count / assignments.count()) * 100)
        return 0
    
    def get_all_assignees(self):
        """获取所有执行人"""
        return [assignment.assignee for assignment in self.assignments.all()]
    
    def get_primary_assignee(self):
        """获取主要执行人（牵头人）"""
        primary_assignment = self.assignments.filter(is_primary=True).first()
        return primary_assignment.assignee if primary_assignment else None


class TaskAssignment(models.Model):
    """
    任务分配表
    记录任务分配给具体执行人的信息
    """
    class AssignmentStatus(models.TextChoices):
        PENDING = 'pending', '待接收'
        ACCEPTED = 'accepted', '已接收'
        IN_PROGRESS = 'in_progress', '进行中'
        COMPLETED = 'completed', '已完成'
        REJECTED = 'rejected', '已拒绝'
    
    class AssignmentRole(models.TextChoices):
        PRIMARY = 'primary', '牵头人'
        COLLABORATOR = 'collaborator', '协助者'
        REVIEWER = 'reviewer', '评审人'
    
    # 关联信息
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='任务'
    )
    assignee = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='task_assignments',
        verbose_name='执行人'
    )
    assignee_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='task_assignments',
        verbose_name='执行人部门'
    )
    
    # 分配信息
    role = models.CharField(
        max_length=20,
        choices=AssignmentRole.choices,
        default=AssignmentRole.COLLABORATOR,
        verbose_name='角色'
    )
    is_primary = models.BooleanField(default=False, verbose_name='是否为牵头人')
    
    # 状态
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.PENDING,
        verbose_name='分配状态'
    )
    
    # 备注
    assignment_note = models.TextField(blank=True, verbose_name='分配备注')
    
    # 时间戳
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name='接收时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        db_table = 'task_assignments'
        verbose_name = '任务分配'
        verbose_name_plural = '任务分配'
        unique_together = [['task', 'assignee']]
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.task.title} -> {self.assignee.real_name}"


class TaskExecution(models.Model):
    """
    任务执行记录
    记录任务执行过程中的详细信息
    """
    class ExecutionStatus(models.TextChoices):
        NOT_STARTED = 'not_started', '未开始'
        IN_PROGRESS = 'in_progress', '进行中'
        PAUSED = 'paused', '暂停'
        COMPLETED = 'completed', '已完成'
        FAILED = 'failed', '失败'
    
    # 关联信息
    assignment = models.OneToOneField(
        TaskAssignment,
        on_delete=models.CASCADE,
        related_name='execution',
        verbose_name='任务分配'
    )
    
    # 执行信息
    status = models.CharField(
        max_length=20,
        choices=ExecutionStatus.choices,
        default=ExecutionStatus.NOT_STARTED,
        verbose_name='执行状态'
    )
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='进度百分比'
    )
    
    # 执行结果
    result_description = models.TextField(blank=True, verbose_name='执行结果描述')
    actual_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='实际工时(小时)'
    )
    
    # 问题和风险
    issues_encountered = models.TextField(blank=True, verbose_name='遇到的问题')
    risks_identified = models.TextField(blank=True, verbose_name='识别的风险')
    
    # 时间戳
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'task_executions'
        verbose_name = '任务执行'
        verbose_name_plural = '任务执行'
    
    def __str__(self):
        return f"{self.assignment.task.title} - {self.assignment.assignee.real_name} 执行记录"


class TaskReview(models.Model):
    """
    任务评价表
    上级对任务执行结果的评价
    """
    class ReviewRating(models.IntegerChoices):
        POOR = 1, '差'
        FAIR = 2, '一般'
        GOOD = 3, '良好'
        EXCELLENT = 4, '优秀'
        OUTSTANDING = 5, '杰出'
    
    # 关联信息
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='任务'
    )
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='task_reviews',
        verbose_name='评价人'
    )
    
    # 评价内容
    rating = models.PositiveIntegerField(
        choices=ReviewRating.choices,
        verbose_name='评分'
    )
    quality_rating = models.PositiveIntegerField(
        choices=ReviewRating.choices,
        verbose_name='质量评分'
    )
    timeliness_rating = models.PositiveIntegerField(
        choices=ReviewRating.choices,
        verbose_name='及时性评分'
    )
    
    # 评价意见
    comments = models.TextField(verbose_name='评价意见')
    suggestions = models.TextField(blank=True, verbose_name='改进建议')
    
    # 是否满意
    is_satisfied = models.BooleanField(default=True, verbose_name='是否满意')
    
    # 时间戳
    reviewed_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')
    
    class Meta:
        db_table = 'task_reviews'
        verbose_name = '任务评价'
        verbose_name_plural = '任务评价'
    
    def __str__(self):
        return f"{self.task.title} - 评价"
    
    @property
    def overall_rating(self):
        """综合评分"""
        return round((self.rating + self.quality_rating + self.timeliness_rating) / 3, 1)


class TaskAttachment(models.Model):
    """
    任务附件表
    """
    class AttachmentType(models.TextChoices):
        TASK_DOCUMENT = 'task_document', '任务文档'
        REFERENCE = 'reference', '参考资料'
        RESULT = 'result', '执行结果'
        IMAGE = 'image', '图片'
        OTHER = 'other', '其他'

    # 关联信息
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='任务'
    )
    uploader = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='uploaded_attachments',
        verbose_name='上传者'
    )

    # 文件信息
    file = models.FileField(upload_to='task_attachments/%Y/%m/', verbose_name='文件')
    original_name = models.CharField(max_length=255, verbose_name='原始文件名')
    file_size = models.PositiveIntegerField(verbose_name='文件大小(字节)')
    file_type = models.CharField(max_length=100, verbose_name='文件类型')

    # 附件属性
    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.TASK_DOCUMENT,
        verbose_name='附件类型'
    )
    description = models.CharField(max_length=200, blank=True, verbose_name='描述')

    # 时间戳
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        db_table = 'task_attachments'
        verbose_name = '任务附件'
        verbose_name_plural = '任务附件'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.task.title} - {self.original_name}"

    @property
    def file_size_display(self):
        """格式化文件大小显示"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class TaskComment(models.Model):
    """
    任务评论表
    """
    class CommentType(models.TextChoices):
        GENERAL = 'general', '一般评论'
        QUESTION = 'question', '问题'
        SUGGESTION = 'suggestion', '建议'
        UPDATE = 'update', '进度更新'

    # 关联信息
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='任务'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='task_comments',
        verbose_name='评论者'
    )

    # 评论内容
    content = models.TextField(verbose_name='评论内容')
    comment_type = models.CharField(
        max_length=20,
        choices=CommentType.choices,
        default=CommentType.GENERAL,
        verbose_name='评论类型'
    )

    # 回复关系
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论'
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'task_comments'
        verbose_name = '任务评论'
        verbose_name_plural = '任务评论'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.task.title} - {self.author.real_name}的评论"


class TaskTemplate(models.Model):
    """
    任务模板表
    用于快速创建常用任务
    """
    class TemplateStatus(models.TextChoices):
        ACTIVE = 'active', '启用'
        INACTIVE = 'inactive', '停用'

    # 基本信息
    name = models.CharField(max_length=100, verbose_name='模板名称')
    description = models.TextField(verbose_name='模板描述')

    # 模板内容
    title_template = models.CharField(max_length=200, verbose_name='标题模板')
    description_template = models.TextField(verbose_name='描述模板')
    task_type = models.CharField(
        max_length=20,
        choices=Task.TaskType.choices,
        default=Task.TaskType.NORMAL,
        verbose_name='任务类型'
    )
    priority = models.CharField(
        max_length=20,
        choices=Task.Priority.choices,
        default=Task.Priority.MEDIUM,
        verbose_name='优先级'
    )
    estimated_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='预估工时(小时)'
    )

    # 创建者和部门
    creator = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='task_templates',
        verbose_name='创建者'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='task_templates',
        verbose_name='所属部门'
    )
    profession = models.ForeignKey(
        'departments.Profession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_templates',
        verbose_name='所属专业'
    )

    # 状态
    status = models.CharField(
        max_length=20,
        choices=TemplateStatus.choices,
        default=TemplateStatus.ACTIVE,
        verbose_name='模板状态'
    )

    # 使用统计
    usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'task_templates'
        verbose_name = '任务模板'
        verbose_name_plural = '任务模板'
        ordering = ['-usage_count', '-created_at']

    def __str__(self):
        return self.name

    def create_task_from_template(self, creator, **kwargs):
        """从模板创建任务"""
        task_data = {
            'title': kwargs.get('title', self.title_template),
            'description': kwargs.get('description', self.description_template),
            'task_type': kwargs.get('task_type', self.task_type),
            'priority': kwargs.get('priority', self.priority),
            'estimated_hours': kwargs.get('estimated_hours', self.estimated_hours),
            'creator': creator,
            'creator_department': creator.department,
            'profession': kwargs.get('profession', self.profession),
            'start_date': kwargs.get('start_date'),
            'due_date': kwargs.get('due_date'),
        }

        task = Task.objects.create(**task_data)

        # 增加使用次数
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

        return task
