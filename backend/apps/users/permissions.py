"""
用户权限类
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    只允许系统管理员访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_admin
        )


class IsAdminOrSelf(permissions.BasePermission):
    """
    只允许系统管理员或用户自己访问
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有用户
        if request.user.is_admin:
            return True
        
        # 用户只能访问自己的信息
        return obj == request.user


class IsDepartmentManager(permissions.BasePermission):
    """
    只允许部门负责人访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_dept_manager)
        )


class IsProfessionManager(permissions.BasePermission):
    """
    只允许专业负责人访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin or 
             request.user.is_dept_manager or 
             request.user.is_prof_manager)
        )


class CanCreateTask(permissions.BasePermission):
    """
    只允许有创建任务权限的用户访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_create_task
        )


class IsTaskCreatorOrAssignee(permissions.BasePermission):
    """
    只允许任务创建者或执行人访问
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有任务
        if request.user.is_admin:
            return True
        
        # 任务创建者可以访问
        if obj.creator == request.user:
            return True
        
        # 任务执行人可以访问
        if obj.assignments.filter(assignee=request.user).exists():
            return True
        
        # 部门负责人可以访问本部门的任务
        if (request.user.is_dept_manager and 
            request.user.department and
            obj.creator_department == request.user.department):
            return True
        
        return False


class IsTaskAssignee(permissions.BasePermission):
    """
    只允许任务执行人访问
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问
        if request.user.is_admin:
            return True
        
        # 检查是否为任务执行人
        if hasattr(obj, 'task'):
            # 对于TaskAssignment等对象
            return obj.assignee == request.user
        elif hasattr(obj, 'assignments'):
            # 对于Task对象
            return obj.assignments.filter(assignee=request.user).exists()
        
        return False
