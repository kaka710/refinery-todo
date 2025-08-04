"""
集成相关序列化器
"""
from rest_framework import serializers
from .models import (
    ShihuatongIntegration, ShihuatongMessage, ShihuatongUserMapping, IntegrationLog
)
from apps.users.serializers import UserSimpleSerializer


class ShihuatongIntegrationSerializer(serializers.ModelSerializer):
    """石化通集成序列化器"""
    success_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ShihuatongIntegration
        fields = [
            'id', 'name', 'description', 'webhook_url', 'app_code',
            'app_key', 'app_secret', 'aes_key', 'aes_iv', 'status',
            'total_messages_sent', 'success_messages_sent', 'failed_messages_sent',
            'success_rate', 'created_at', 'updated_at', 'last_used_at'
        ]
        read_only_fields = [
            'total_messages_sent', 'success_messages_sent', 'failed_messages_sent',
            'success_rate', 'created_at', 'updated_at', 'last_used_at'
        ]
        extra_kwargs = {
            'app_secret': {'write_only': True},
            'aes_key': {'write_only': True},
            'aes_iv': {'write_only': True}
        }


class ShihuatongIntegrationSimpleSerializer(serializers.ModelSerializer):
    """石化通集成简单序列化器"""
    success_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ShihuatongIntegration
        fields = ['id', 'name', 'status', 'success_rate', 'last_used_at']


class ShihuatongMessageSerializer(serializers.ModelSerializer):
    """石化通消息序列化器"""
    integration_name = serializers.CharField(source='integration.name', read_only=True)
    related_task_title = serializers.CharField(
        source='related_task.title', read_only=True
    )
    
    class Meta:
        model = ShihuatongMessage
        fields = [
            'id', 'integration', 'integration_name', 'message_type',
            'title', 'content', 'hook_token', 'recipient_user_ids',
            'mention_all', 'related_task', 'related_task_title',
            'related_notification', 'status', 'response_data',
            'error_message', 'retry_count', 'max_retries',
            'created_at', 'sent_at'
        ]
        read_only_fields = [
            'response_data', 'error_message', 'retry_count',
            'created_at', 'sent_at'
        ]


class ShihuatongMessageCreateSerializer(serializers.ModelSerializer):
    """石化通消息创建序列化器"""
    
    class Meta:
        model = ShihuatongMessage
        fields = [
            'integration', 'message_type', 'title', 'content',
            'hook_token', 'recipient_user_ids', 'mention_all',
            'related_task', 'related_notification'
        ]
    
    def validate_recipient_user_ids(self, value):
        """验证接收用户ID列表"""
        if not isinstance(value, list):
            raise serializers.ValidationError('接收用户ID必须是列表格式')
        
        if not value and not self.initial_data.get('mention_all', False):
            raise serializers.ValidationError('必须指定接收用户或选择@所有人')
        
        return value


class ShihuatongUserMappingSerializer(serializers.ModelSerializer):
    """石化通用户映射序列化器"""
    user = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = ShihuatongUserMapping
        fields = [
            'id', 'user', 'shihuatong_user_id', 'shihuatong_username',
            'shihuatong_display_name', 'default_hook_token', 'status',
            'verified_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'verified_at', 'created_at', 'updated_at']


class ShihuatongUserMappingCreateSerializer(serializers.ModelSerializer):
    """石化通用户映射创建序列化器"""
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ShihuatongUserMapping
        fields = [
            'user_id', 'shihuatong_user_id', 'shihuatong_username',
            'shihuatong_display_name', 'default_hook_token'
        ]
    
    def validate_user_id(self, value):
        """验证用户ID"""
        from apps.users.models import User
        
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('指定的用户不存在')
    
    def create(self, validated_data):
        """创建映射时设置用户"""
        from apps.users.models import User
        
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        
        return ShihuatongUserMapping.objects.create(
            user=user,
            **validated_data
        )


class IntegrationLogSerializer(serializers.ModelSerializer):
    """集成日志序列化器"""
    integration_name = serializers.CharField(source='integration.name', read_only=True)
    
    class Meta:
        model = IntegrationLog
        fields = [
            'id', 'integration', 'integration_name', 'level',
            'operation_type', 'message', 'request_data',
            'response_data', 'execution_time', 'created_at'
        ]
        read_only_fields = ['created_at']


class ShihuatongStatsSerializer(serializers.Serializer):
    """石化通统计序列化器"""
    total_integrations = serializers.IntegerField()
    active_integrations = serializers.IntegerField()
    total_messages = serializers.IntegerField()
    success_messages = serializers.IntegerField()
    failed_messages = serializers.IntegerField()
    success_rate = serializers.FloatField()
    recent_messages = ShihuatongMessageSerializer(many=True)


class SendMessageSerializer(serializers.Serializer):
    """发送消息序列化器"""
    hook_token = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    message_type = serializers.ChoiceField(
        choices=ShihuatongMessage.MessageType.choices,
        default='text'
    )
    mention_all = serializers.BooleanField(default=False)
    user_ids = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    related_task_id = serializers.UUIDField(required=False)
    integration_id = serializers.IntegerField(required=False)
