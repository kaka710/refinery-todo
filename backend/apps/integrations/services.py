"""
石化通集成服务
基于提供的示例代码实现石化通消息推送功能
"""
import requests
import json
import datetime
import hmac
import hashlib
import base64
import uuid
import urllib.parse
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .models import ShihuatongIntegration, ShihuatongMessage, IntegrationLog

logger = logging.getLogger(__name__)


class ShihuatongService:
    """
    石化通消息推送服务
    """
    
    def __init__(self, integration_id: Optional[int] = None):
        """
        初始化服务
        
        Args:
            integration_id: 集成配置ID，如果不提供则使用默认配置
        """
        if integration_id:
            try:
                self.integration = ShihuatongIntegration.objects.get(
                    id=integration_id,
                    status=ShihuatongIntegration.IntegrationStatus.ACTIVE
                )
            except ShihuatongIntegration.DoesNotExist:
                raise ValueError(f"集成配置 {integration_id} 不存在或未启用")
        else:
            # 使用默认配置或从settings获取
            self.integration = self._get_default_integration()
    
    def _get_default_integration(self) -> ShihuatongIntegration:
        """获取默认集成配置"""
        # 首先尝试从数据库获取默认配置
        integration = ShihuatongIntegration.objects.filter(
            status=ShihuatongIntegration.IntegrationStatus.ACTIVE
        ).first()
        
        if not integration:
            # 如果数据库中没有配置，从settings创建默认配置
            config = settings.SHIHUATONG_CONFIG
            integration = ShihuatongIntegration.objects.create(
                name='默认石化通集成',
                webhook_url=config.get('WEBHOOK_URL', ''),
                app_code=config.get('APP_CODE', ''),
                app_key=config.get('APP_KEY', ''),
                app_secret=config.get('APP_SECRET', ''),
                aes_key=config.get('AES_KEY', ''),
                aes_iv=config.get('AES_IV', ''),
            )
        
        return integration
    
    def _encrypt_aes(self, data: str) -> str:
        """
        AES CBC加密

        Args:
            data: 待加密的数据

        Returns:
            加密后的base64字符串
        """
        try:
            # 从base64编码的密钥和IV中解码出原始字节
            key = base64.b64decode(self.integration.aes_key)
            iv = base64.b64decode(self.integration.aes_iv)

            # 填充数据
            padded_data = pad(data.encode('utf-8'), AES.block_size)

            # 创建加密器
            cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

            # 加密并转换为base64
            encrypted = cipher.encrypt(padded_data)
            result = base64.b64encode(encrypted).decode('utf-8')

            return result
        except Exception as e:
            logger.error(f"AES加密失败: {e}")
            raise
    
    def _url_encode(self, text: str) -> str:
        """URL编码"""
        return urllib.parse.quote(text, safe='')
    
    def _get_hmac_signature(self, data: str) -> str:
        """
        生成HMAC SHA256签名
        
        Args:
            data: 待签名的数据
            
        Returns:
            签名字符串
        """
        try:
            key = self.integration.app_secret.encode('utf-8')
            data_bytes = data.encode('utf-8')
            
            hmac_sha256 = hmac.new(key, data_bytes, digestmod=hashlib.sha256)
            hash_bytes = hmac_sha256.digest()
            
            return base64.b64encode(hash_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"HMAC签名生成失败: {e}")
            raise
    
    def _get_content_sha256(self, content: str) -> str:
        """
        计算内容的SHA256哈希
        
        Args:
            content: 内容字符串
            
        Returns:
            SHA256哈希值的base64编码
        """
        try:
            content_bytes = content.encode('utf-8')
            sha256_hash = hashlib.sha256(content_bytes).digest()
            return base64.b64encode(sha256_hash).decode('utf-8').replace('-', '').lower()
        except Exception as e:
            logger.error(f"SHA256计算失败: {e}")
            raise
    
    def _get_gmt_time(self) -> str:
        """获取GMT时间字符串"""
        # 获取当前CST时间
        cst_time = datetime.datetime.now()
        # 转换为GMT时间
        gmt_time = cst_time - datetime.timedelta(hours=8)
        # 格式化为字符串
        return gmt_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    def _build_message_data(
        self,
        hook_token: str,
        title: str,
        content: str,
        message_type: str = 'text',
        mention_all: bool = False,
        user_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        构建消息数据
        
        Args:
            hook_token: Hook Token
            title: 消息标题
            content: 消息内容
            message_type: 消息类型
            mention_all: 是否@所有人
            user_ids: 指定用户ID列表
            
        Returns:
            消息数据字典
        """
        msg_id = str(uuid.uuid4())
        
        # 构建消息内容
        send_content = f"{title}\n{content}"
        
        # 构建提醒信息
        reminder = {
            "all": mention_all,
            "userIds": user_ids or []
        }
        
        # 构建消息数据
        if message_type == 'text':
            data_content = {
                "text": {
                    "content": self._url_encode(send_content),
                    "reminder": reminder
                }
            }
        else:
            # 可以扩展支持其他消息类型
            data_content = {
                "text": {
                    "content": self._url_encode(send_content),
                    "reminder": reminder
                }
            }
        
        message_data = {
            "sendType": 1,
            "hook_token": hook_token,
            "appId": "",
            "appSecret": "",
            "secret": "替换为自己群组机器人安全设置-加签的密钥",
            "id": msg_id,
            "msgType": message_type,
            "data": json.dumps(data_content, ensure_ascii=False)
        }
        
        return message_data, msg_id
    
    def send_message(
        self,
        hook_token: str,
        title: str,
        content: str,
        message_type: str = 'text',
        mention_all: bool = False,
        user_ids: Optional[List[str]] = None,
        related_task_id: Optional[str] = None,
        related_notification_id: Optional[str] = None
    ) -> ShihuatongMessage:
        """
        发送石化通消息
        
        Args:
            hook_token: Hook Token
            title: 消息标题
            content: 消息内容
            message_type: 消息类型
            mention_all: 是否@所有人
            user_ids: 指定用户ID列表
            related_task_id: 关联任务ID
            related_notification_id: 关联通知ID
            
        Returns:
            ShihuatongMessage实例
        """
        # 创建消息记录
        message = ShihuatongMessage.objects.create(
            integration=self.integration,
            message_type=message_type,
            title=title,
            content=content,
            hook_token=hook_token,
            recipient_user_ids=user_ids or [],
            mention_all=mention_all,
            related_task_id=related_task_id,
            related_notification_id=related_notification_id,
            status=ShihuatongMessage.MessageStatus.PENDING
        )
        
        try:
            # 构建消息数据
            message_data, msg_id = self._build_message_data(
                hook_token, title, content, message_type, mention_all, user_ids
            )
            
            # 加密消息内容
            encrypted_content = self._encrypt_aes(json.dumps(message_data, ensure_ascii=False))
            
            # 构建请求数据
            request_data = {
                "content": encrypted_content,
                "appCode": self.integration.app_code
            }
            
            # 计算请求内容哈希
            content_sha256 = self._get_content_sha256(json.dumps(request_data, ensure_ascii=False))
            
            # 获取GMT时间
            gmt_time = self._get_gmt_time()
            
            # 构建签名字符串
            signature_str = f'x-date: {gmt_time}\ncontent-sha256: {content_sha256}'
            
            # 生成HMAC签名
            signature = self._get_hmac_signature(signature_str)
            
            # 构建Authorization头
            auth_header = (
                f'hmac accesskey="{self.integration.app_key}", '
                f'algorithm="hmac-sha256", '
                f'headers="x-date content-sha256", '
                f'signature="{signature}"'
            )
            
            # 构建请求头
            headers = {
                "Authorization": auth_header,
                "X-Date": gmt_time,
                "Content-sha256": content_sha256,
                "Content-Type": "application/json"
            }
            
            # 更新消息状态为发送中
            message.status = ShihuatongMessage.MessageStatus.SENDING
            message.save(update_fields=['status'])
            
            # 发送HTTP请求
            response = requests.post(
                url=self.integration.webhook_url,
                data=json.dumps(request_data, ensure_ascii=False),
                headers=headers,
                timeout=30
            )
            
            # 处理响应
            response_data = response.json() if response.content else {}
            
            if response.status_code == 200:
                result = response_data
                if result.get("status") == "0":
                    # 发送成功
                    message.status = ShihuatongMessage.MessageStatus.SUCCESS
                    message.response_data = response_data
                    message.sent_at = datetime.datetime.now()
                    
                    # 更新集成统计
                    self.integration.total_messages_sent += 1
                    self.integration.success_messages_sent += 1
                    self.integration.last_used_at = datetime.datetime.now()
                    self.integration.save()
                    
                    # 记录成功日志
                    self._log_operation(
                        level=IntegrationLog.LogLevel.INFO,
                        operation_type=IntegrationLog.OperationType.SEND_MESSAGE,
                        message=f"消息发送成功: {title}",
                        request_data=request_data,
                        response_data=response_data
                    )
                else:
                    # 发送失败
                    message.status = ShihuatongMessage.MessageStatus.FAILED
                    message.error_message = result.get("failureMsg", "未知错误")
                    message.response_data = response_data
                    
                    # 更新集成统计
                    self.integration.total_messages_sent += 1
                    self.integration.failed_messages_sent += 1
                    self.integration.save()
                    
                    # 记录错误日志
                    self._log_operation(
                        level=IntegrationLog.LogLevel.ERROR,
                        operation_type=IntegrationLog.OperationType.SEND_MESSAGE,
                        message=f"消息发送失败: {message.error_message}",
                        request_data=request_data,
                        response_data=response_data
                    )
            else:
                # HTTP请求失败
                message.status = ShihuatongMessage.MessageStatus.FAILED
                message.error_message = f"HTTP {response.status_code}: {response.text}"
                message.response_data = {"status_code": response.status_code, "text": response.text}
                
                # 更新集成统计
                self.integration.total_messages_sent += 1
                self.integration.failed_messages_sent += 1
                self.integration.save()
                
                # 记录错误日志
                self._log_operation(
                    level=IntegrationLog.LogLevel.ERROR,
                    operation_type=IntegrationLog.OperationType.SEND_MESSAGE,
                    message=f"HTTP请求失败: {response.status_code}",
                    request_data=request_data,
                    response_data=message.response_data
                )
            
            message.save()
            
        except Exception as e:
            # 异常处理
            message.status = ShihuatongMessage.MessageStatus.FAILED
            message.error_message = str(e)
            message.save()
            
            # 更新集成统计
            self.integration.total_messages_sent += 1
            self.integration.failed_messages_sent += 1
            self.integration.save()
            
            # 记录错误日志
            self._log_operation(
                level=IntegrationLog.LogLevel.ERROR,
                operation_type=IntegrationLog.OperationType.SEND_MESSAGE,
                message=f"发送异常: {str(e)}",
                request_data={},
                response_data={}
            )
            
            logger.error(f"石化通消息发送异常: {e}", exc_info=True)
        
        return message
    
    def _log_operation(
        self,
        level: str,
        operation_type: str,
        message: str,
        request_data: Dict = None,
        response_data: Dict = None,
        execution_time: float = None
    ):
        """记录操作日志"""
        IntegrationLog.objects.create(
            integration=self.integration,
            level=level,
            operation_type=operation_type,
            message=message,
            request_data=request_data or {},
            response_data=response_data or {},
            execution_time=execution_time
        )
    
    def retry_failed_message(self, message_id: str) -> bool:
        """
        重试失败的消息
        
        Args:
            message_id: 消息ID
            
        Returns:
            是否重试成功
        """
        try:
            message = ShihuatongMessage.objects.get(id=message_id)
            
            if not message.can_retry:
                return False
            
            # 增加重试次数
            message.retry_count += 1
            message.status = ShihuatongMessage.MessageStatus.RETRY
            message.save()
            
            # 重新发送
            new_message = self.send_message(
                hook_token=message.hook_token,
                title=message.title,
                content=message.content,
                message_type=message.message_type,
                mention_all=message.mention_all,
                user_ids=message.recipient_user_ids,
                related_task_id=message.related_task_id,
                related_notification_id=message.related_notification_id
            )
            
            return new_message.status == ShihuatongMessage.MessageStatus.SUCCESS
            
        except Exception as e:
            logger.error(f"重试消息失败: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            健康状态信息
        """
        try:
            # 发送测试消息
            test_message = self.send_message(
                hook_token="test",
                title="健康检查",
                content="这是一条测试消息",
                message_type="text"
            )
            
            status = "healthy" if test_message.status == ShihuatongMessage.MessageStatus.SUCCESS else "unhealthy"
            
            return {
                "status": status,
                "integration_id": self.integration.id,
                "integration_name": self.integration.name,
                "success_rate": self.integration.success_rate,
                "last_used_at": self.integration.last_used_at,
                "test_message_id": str(test_message.id)
            }
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
