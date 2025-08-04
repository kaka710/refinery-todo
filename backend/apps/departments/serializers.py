"""
部门相关序列化器
"""
from rest_framework import serializers
from .models import Department, Profession, DepartmentCollaboration


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'parent', 'parent_name',
            'level', 'type', 'status', 'phone', 'email', 'address', 'sort_order',
            'children_count', 'users_count', 'full_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['level', 'full_name', 'created_at', 'updated_at']
    
    def get_children_count(self, obj):
        """获取子部门数量"""
        return obj.children.filter(status=Department.DepartmentStatus.ACTIVE).count()
    
    def get_users_count(self, obj):
        """获取部门用户数量"""
        return obj.users.filter(status='active').count()
    
    def validate(self, attrs):
        """验证数据"""
        parent = attrs.get('parent')
        
        # 检查父部门循环引用
        if parent and self.instance:
            current = parent
            while current:
                if current == self.instance:
                    raise serializers.ValidationError('不能将自己设置为父部门')
                current = current.parent
        
        return attrs


class DepartmentTreeSerializer(serializers.ModelSerializer):
    """部门树形序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'type', 'status',
            'sort_order', 'children'
        ]
    
    def get_children(self, obj):
        """获取子部门"""
        children = obj.children.filter(
            status=Department.DepartmentStatus.ACTIVE
        ).order_by('sort_order', 'name')
        
        return DepartmentTreeSerializer(children, many=True).data


class DepartmentSimpleSerializer(serializers.ModelSerializer):
    """部门简单序列化器"""
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'full_name']


class ProfessionSerializer(serializers.ModelSerializer):
    """专业序列化器"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Profession
        fields = [
            'id', 'name', 'code', 'description', 'department', 'department_name',
            'status', 'sort_order', 'users_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_users_count(self, obj):
        """获取专业相关用户数量"""
        return obj.get_users().count()


class ProfessionSimpleSerializer(serializers.ModelSerializer):
    """专业简单序列化器"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Profession
        fields = ['id', 'name', 'code', 'department_name']


class DepartmentCollaborationSerializer(serializers.ModelSerializer):
    """部门协作关系序列化器"""
    primary_department_name = serializers.CharField(
        source='primary_department.name', read_only=True
    )
    secondary_department_name = serializers.CharField(
        source='secondary_department.name', read_only=True
    )
    
    class Meta:
        model = DepartmentCollaboration
        fields = [
            'id', 'primary_department', 'primary_department_name',
            'secondary_department', 'secondary_department_name',
            'collaboration_type', 'description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        """验证数据"""
        primary_dept = attrs.get('primary_department')
        secondary_dept = attrs.get('secondary_department')
        
        if primary_dept == secondary_dept:
            raise serializers.ValidationError('主导部门和协作部门不能相同')
        
        return attrs


class DepartmentStatsSerializer(serializers.Serializer):
    """部门统计序列化器"""
    department_id = serializers.IntegerField()
    department_name = serializers.CharField()
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
