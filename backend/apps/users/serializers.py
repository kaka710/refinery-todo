"""
用户相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile, UserLoginLog
from apps.departments.models import Department


class DepartmentSimpleSerializer(serializers.ModelSerializer):
    """部门简单序列化器"""
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'full_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'position', 'office_location',
            'email_notifications', 'sms_notifications', 'shihuatong_notifications'
        ]


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    department = DepartmentSimpleSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True, required=False)
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password], required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'employee_id', 'real_name', 'email', 'phone',
            'role', 'status', 'department', 'department_id', 'profile', 'password',
            'is_active', 'date_joined', 'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'employee_id': {'required': False},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }
    
    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """更新用户"""
        password = validated_data.pop('password', None)

        # 处理部门字段
        department_id = validated_data.pop('department_id', None)
        if department_id:
            from apps.departments.models import Department
            try:
                department = Department.objects.get(id=department_id)
                instance.department = department
            except Department.DoesNotExist:
                pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简单序列化器"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'employee_id', 'real_name', 'role', 'department_name']


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # 支持用户名或工号登录
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                # 尝试用工号登录
                try:
                    user_obj = User.objects.get(employee_id=username)
                    user = authenticate(
                        request=self.context.get('request'),
                        username=user_obj.username,
                        password=password
                    )
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            
            if not user.is_active:
                raise serializers.ValidationError('用户账号已被禁用')
            
            if user.status != User.UserStatus.ACTIVE:
                raise serializers.ValidationError('用户状态异常，请联系管理员')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('必须提供用户名和密码')


class TokenSerializer(serializers.Serializer):
    """Token序列化器"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'employee_id', 'real_name', 'email', 'phone',
            'password', 'confirm_password', 'department_id'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('两次输入的密码不一致')
        
        # 验证部门是否存在
        try:
            department = Department.objects.get(id=attrs['department_id'])
            attrs['department'] = department
        except Department.DoesNotExist:
            raise serializers.ValidationError('指定的部门不存在')
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        department = validated_data.pop('department')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            department=department,
            **validated_data
        )
        user.set_password(password)
        user.save()
        
        return user


class UserLoginLogSerializer(serializers.ModelSerializer):
    """用户登录日志序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    
    class Meta:
        model = UserLoginLog
        fields = [
            'id', 'user_name', 'ip_address', 'user_agent',
            'login_time', 'is_success', 'failure_reason'
        ]


class UserPermissionSerializer(serializers.Serializer):
    """用户权限序列化器"""
    can_create_task = serializers.BooleanField(read_only=True)
    can_manage_users = serializers.BooleanField(read_only=True)
    managed_departments = DepartmentSimpleSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        return {
            'can_create_task': instance.can_create_task,
            'can_manage_users': instance.can_manage_users,
            'managed_departments': DepartmentSimpleSerializer(
                instance.get_managed_departments(), many=True
            ).data
        }
