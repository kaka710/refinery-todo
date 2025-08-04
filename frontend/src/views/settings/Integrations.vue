<template>
  <div class="integrations">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Connection /></el-icon>
        集成设置
      </h1>
      <p class="page-subtitle">管理第三方服务集成和API配置</p>
    </div>

    <div class="integrations-content">
      <el-row :gutter="24">
        <!-- 左侧集成列表 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <div class="integration-panels">
            <!-- 石化通集成 -->
            <el-card class="integration-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div class="integration-info">
                    <el-icon class="integration-icon shihuatong"><Connection /></el-icon>
                    <div>
                      <h3 class="integration-title">石化通集成</h3>
                      <p class="integration-description">与石化通系统集成，实现单点登录和消息推送</p>
                    </div>
                  </div>
                  <div class="integration-status">
                    <el-tag :type="shihuatongConfig.enabled ? 'success' : 'info'" size="small">
                      {{ shihuatongConfig.enabled ? '已启用' : '未启用' }}
                    </el-tag>
                  </div>
                </div>
              </template>

              <div class="integration-content">
                <el-form :model="shihuatongConfig" label-width="120px" class="integration-form">
                  <el-form-item label="启用集成">
                    <el-switch
                      v-model="shihuatongConfig.enabled"
                      @change="handleShihuatongToggle"
                    />
                    <div class="form-tip">启用后可使用石化通账号登录</div>
                  </el-form-item>

                  <template v-if="shihuatongConfig.enabled">
                    <el-form-item label="服务器地址" required>
                      <el-input
                        v-model="shihuatongConfig.server_url"
                        placeholder="请输入石化通服务器地址"
                      />
                    </el-form-item>

                    <el-form-item label="应用ID" required>
                      <el-input
                        v-model="shihuatongConfig.app_id"
                        placeholder="请输入应用ID"
                      />
                    </el-form-item>

                    <el-form-item label="应用密钥" required>
                      <el-input
                        v-model="shihuatongConfig.app_secret"
                        type="password"
                        placeholder="请输入应用密钥"
                        show-password
                      />
                    </el-form-item>

                    <el-form-item label="消息推送">
                      <el-checkbox v-model="shihuatongConfig.enable_push">
                        启用消息推送到石化通
                      </el-checkbox>
                    </el-form-item>

                    <el-form-item label="同步用户">
                      <el-checkbox v-model="shihuatongConfig.sync_users">
                        自动同步用户信息
                      </el-checkbox>
                    </el-form-item>
                  </template>
                </el-form>

                <div class="integration-actions">
                  <el-button
                    v-if="shihuatongConfig.enabled"
                    type="primary"
                    @click="testShihuatongConnection"
                    :loading="testing.shihuatong"
                  >
                    测试连接
                  </el-button>
                  <el-button
                    type="primary"
                    @click="saveShihuatongConfig"
                    :loading="saving.shihuatong"
                  >
                    保存配置
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- 邮件服务配置 -->
            <el-card class="integration-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div class="integration-info">
                    <el-icon class="integration-icon email"><Message /></el-icon>
                    <div>
                      <h3 class="integration-title">邮件服务</h3>
                      <p class="integration-description">配置SMTP服务器用于发送邮件通知</p>
                    </div>
                  </div>
                  <div class="integration-status">
                    <el-tag :type="emailConfig.enabled ? 'success' : 'info'" size="small">
                      {{ emailConfig.enabled ? '已启用' : '未启用' }}
                    </el-tag>
                  </div>
                </div>
              </template>

              <div class="integration-content">
                <el-form :model="emailConfig" label-width="120px" class="integration-form">
                  <el-form-item label="启用邮件">
                    <el-switch
                      v-model="emailConfig.enabled"
                      @change="handleEmailToggle"
                    />
                    <div class="form-tip">启用后可发送邮件通知</div>
                  </el-form-item>

                  <template v-if="emailConfig.enabled">
                    <el-form-item label="SMTP服务器" required>
                      <el-input
                        v-model="emailConfig.smtp_host"
                        placeholder="例如：smtp.qq.com"
                      />
                    </el-form-item>

                    <el-form-item label="端口号" required>
                      <el-input-number
                        v-model="emailConfig.smtp_port"
                        :min="1"
                        :max="65535"
                        placeholder="例如：587"
                      />
                    </el-form-item>

                    <el-form-item label="用户名" required>
                      <el-input
                        v-model="emailConfig.smtp_user"
                        placeholder="请输入邮箱用户名"
                      />
                    </el-form-item>

                    <el-form-item label="密码" required>
                      <el-input
                        v-model="emailConfig.smtp_password"
                        type="password"
                        placeholder="请输入邮箱密码或授权码"
                        show-password
                      />
                    </el-form-item>

                    <el-form-item label="发件人名称">
                      <el-input
                        v-model="emailConfig.from_name"
                        placeholder="例如：海南炼化Todo系统"
                      />
                    </el-form-item>

                    <el-form-item label="发件人邮箱">
                      <el-input
                        v-model="emailConfig.from_email"
                        placeholder="例如：noreply@company.com"
                      />
                    </el-form-item>

                    <el-form-item label="加密方式">
                      <el-radio-group v-model="emailConfig.encryption">
                        <el-radio value="none">无加密</el-radio>
                        <el-radio value="tls">TLS</el-radio>
                        <el-radio value="ssl">SSL</el-radio>
                      </el-radio-group>
                    </el-form-item>
                  </template>
                </el-form>

                <div class="integration-actions">
                  <el-button
                    v-if="emailConfig.enabled"
                    type="primary"
                    @click="testEmailConnection"
                    :loading="testing.email"
                  >
                    发送测试邮件
                  </el-button>
                  <el-button
                    type="primary"
                    @click="saveEmailConfig"
                    :loading="saving.email"
                  >
                    保存配置
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- 短信服务配置 -->
            <el-card class="integration-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div class="integration-info">
                    <el-icon class="integration-icon sms"><ChatDotRound /></el-icon>
                    <div>
                      <h3 class="integration-title">短信服务</h3>
                      <p class="integration-description">配置短信服务商用于发送短信通知</p>
                    </div>
                  </div>
                  <div class="integration-status">
                    <el-tag :type="smsConfig.enabled ? 'success' : 'info'" size="small">
                      {{ smsConfig.enabled ? '已启用' : '未启用' }}
                    </el-tag>
                  </div>
                </div>
              </template>

              <div class="integration-content">
                <el-form :model="smsConfig" label-width="120px" class="integration-form">
                  <el-form-item label="启用短信">
                    <el-switch
                      v-model="smsConfig.enabled"
                      @change="handleSmsToggle"
                    />
                    <div class="form-tip">启用后可发送短信通知</div>
                  </el-form-item>

                  <template v-if="smsConfig.enabled">
                    <el-form-item label="服务商" required>
                      <el-select v-model="smsConfig.provider" style="width: 100%">
                        <el-option label="阿里云短信" value="aliyun" />
                        <el-option label="腾讯云短信" value="tencent" />
                        <el-option label="华为云短信" value="huawei" />
                      </el-select>
                    </el-form-item>

                    <el-form-item label="Access Key" required>
                      <el-input
                        v-model="smsConfig.access_key"
                        placeholder="请输入Access Key"
                      />
                    </el-form-item>

                    <el-form-item label="Secret Key" required>
                      <el-input
                        v-model="smsConfig.secret_key"
                        type="password"
                        placeholder="请输入Secret Key"
                        show-password
                      />
                    </el-form-item>

                    <el-form-item label="签名" required>
                      <el-input
                        v-model="smsConfig.sign_name"
                        placeholder="请输入短信签名"
                      />
                    </el-form-item>

                    <el-form-item label="模板ID" required>
                      <el-input
                        v-model="smsConfig.template_id"
                        placeholder="请输入短信模板ID"
                      />
                    </el-form-item>
                  </template>
                </el-form>

                <div class="integration-actions">
                  <el-button
                    v-if="smsConfig.enabled"
                    type="primary"
                    @click="testSmsConnection"
                    :loading="testing.sms"
                  >
                    发送测试短信
                  </el-button>
                  <el-button
                    type="primary"
                    @click="saveSmsConfig"
                    :loading="saving.sms"
                  >
                    保存配置
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- API接口管理 -->
            <el-card class="integration-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div class="integration-info">
                    <el-icon class="integration-icon api"><Setting /></el-icon>
                    <div>
                      <h3 class="integration-title">API接口管理</h3>
                      <p class="integration-description">管理API密钥和访问权限</p>
                    </div>
                  </div>
                  <el-button type="primary" size="small" @click="showCreateApiKey = true">
                    创建API密钥
                  </el-button>
                </div>
              </template>

              <div class="integration-content">
                <div class="api-keys-list">
                  <div
                    v-for="apiKey in apiKeys"
                    :key="apiKey.id"
                    class="api-key-item"
                  >
                    <div class="api-key-info">
                      <div class="api-key-header">
                        <h4 class="api-key-name">{{ apiKey.name }}</h4>
                        <el-tag :type="apiKey.status === 'active' ? 'success' : 'danger'" size="small">
                          {{ apiKey.status === 'active' ? '活跃' : '已禁用' }}
                        </el-tag>
                      </div>
                      <div class="api-key-details">
                        <p class="api-key-description">{{ apiKey.description }}</p>
                        <div class="api-key-meta">
                          <span>创建时间：{{ formatDate(apiKey.created_at) }}</span>
                          <span>最后使用：{{ formatDate(apiKey.last_used_at) }}</span>
                          <span>使用次数：{{ apiKey.usage_count }}</span>
                        </div>
                      </div>
                    </div>
                    <div class="api-key-actions">
                      <el-button size="small" @click="viewApiKey(apiKey)">查看</el-button>
                      <el-button
                        size="small"
                        :type="apiKey.status === 'active' ? 'warning' : 'success'"
                        @click="toggleApiKey(apiKey)"
                      >
                        {{ apiKey.status === 'active' ? '禁用' : '启用' }}
                      </el-button>
                      <el-button size="small" type="danger" @click="deleteApiKey(apiKey)">
                        删除
                      </el-button>
                    </div>
                  </div>

                  <div v-if="apiKeys.length === 0" class="empty-api-keys">
                    <el-empty description="暂无API密钥" />
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>

        <!-- 右侧状态和日志 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <div class="status-panel">
            <!-- 集成状态 -->
            <el-card class="status-card" shadow="never">
              <template #header>
                <span>集成状态</span>
              </template>

              <div class="status-list">
                <div class="status-item">
                  <div class="status-info">
                    <el-icon class="status-icon shihuatong"><Connection /></el-icon>
                    <span class="status-name">石化通</span>
                  </div>
                  <div class="status-indicator">
                    <el-tag :type="shihuatongConfig.enabled ? 'success' : 'info'" size="small">
                      {{ shihuatongConfig.enabled ? '已连接' : '未连接' }}
                    </el-tag>
                  </div>
                </div>

                <div class="status-item">
                  <div class="status-info">
                    <el-icon class="status-icon email"><Message /></el-icon>
                    <span class="status-name">邮件服务</span>
                  </div>
                  <div class="status-indicator">
                    <el-tag :type="emailConfig.enabled ? 'success' : 'info'" size="small">
                      {{ emailConfig.enabled ? '已配置' : '未配置' }}
                    </el-tag>
                  </div>
                </div>

                <div class="status-item">
                  <div class="status-info">
                    <el-icon class="status-icon sms"><ChatDotRound /></el-icon>
                    <span class="status-name">短信服务</span>
                  </div>
                  <div class="status-indicator">
                    <el-tag :type="smsConfig.enabled ? 'success' : 'info'" size="small">
                      {{ smsConfig.enabled ? '已配置' : '未配置' }}
                    </el-tag>
                  </div>
                </div>

                <div class="status-item">
                  <div class="status-info">
                    <el-icon class="status-icon api"><Setting /></el-icon>
                    <span class="status-name">API接口</span>
                  </div>
                  <div class="status-indicator">
                    <el-tag type="success" size="small">
                      {{ apiKeys.filter(k => k.status === 'active').length }} 个活跃
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 使用统计 -->
            <el-card class="stats-card" shadow="never">
              <template #header>
                <span>使用统计</span>
              </template>

              <div class="stats-list">
                <div class="stats-item">
                  <div class="stats-label">今日邮件发送</div>
                  <div class="stats-value">{{ usageStats.email_today }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">今日短信发送</div>
                  <div class="stats-value">{{ usageStats.sms_today }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">API调用次数</div>
                  <div class="stats-value">{{ usageStats.api_calls }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">石化通推送</div>
                  <div class="stats-value">{{ usageStats.shihuatong_push }}</div>
                </div>
              </div>
            </el-card>

            <!-- 最近日志 -->
            <el-card class="logs-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>最近日志</span>
                  <el-button size="small" @click="refreshLogs">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </div>
              </template>

              <div class="logs-list">
                <div
                  v-for="log in recentLogs"
                  :key="log.id"
                  class="log-item"
                  :class="log.level"
                >
                  <div class="log-header">
                    <span class="log-service">{{ log.service }}</span>
                    <span class="log-time">{{ formatTime(log.created_at) }}</span>
                  </div>
                  <div class="log-message">{{ log.message }}</div>
                </div>

                <div v-if="recentLogs.length === 0" class="empty-logs">
                  <p>暂无日志记录</p>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 创建API密钥对话框 -->
    <el-dialog
      v-model="showCreateApiKey"
      title="创建API密钥"
      width="500px"
    >
      <el-form :model="newApiKey" label-width="100px">
        <el-form-item label="密钥名称" required>
          <el-input v-model="newApiKey.name" placeholder="请输入密钥名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="newApiKey.description"
            type="textarea"
            :rows="3"
            placeholder="请输入密钥描述"
          />
        </el-form-item>
        <el-form-item label="权限范围">
          <el-checkbox-group v-model="newApiKey.permissions">
            <el-checkbox value="read">只读权限</el-checkbox>
            <el-checkbox value="write">写入权限</el-checkbox>
            <el-checkbox value="admin">管理权限</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="过期时间">
          <el-select v-model="newApiKey.expires_in" style="width: 100%">
            <el-option label="30天" :value="30" />
            <el-option label="90天" :value="90" />
            <el-option label="180天" :value="180" />
            <el-option label="365天" :value="365" />
            <el-option label="永不过期" :value="0" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateApiKey = false">取消</el-button>
        <el-button type="primary" @click="createApiKey" :loading="creating">
          创建
        </el-button>
      </template>
    </el-dialog>

    <!-- API密钥详情对话框 -->
    <el-dialog
      v-model="showApiKeyDetail"
      title="API密钥详情"
      width="600px"
    >
      <div v-if="selectedApiKey" class="api-key-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="密钥名称">{{ selectedApiKey.name }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedApiKey.status === 'active' ? 'success' : 'danger'" size="small">
              {{ selectedApiKey.status === 'active' ? '活跃' : '已禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="API密钥" span="2">
            <div class="api-key-value">
              <el-input
                :value="selectedApiKey.key"
                readonly
                type="password"
                show-password
              />
              <el-button size="small" @click="copyApiKey(selectedApiKey.key)">
                复制
              </el-button>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="权限范围" span="2">
            <el-tag
              v-for="permission in selectedApiKey.permissions"
              :key="permission"
              size="small"
              style="margin-right: 8px"
            >
              {{ getPermissionText(permission) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(selectedApiKey.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="过期时间">
            {{ selectedApiKey.expires_at ? formatDateTime(selectedApiKey.expires_at) : '永不过期' }}
          </el-descriptions-item>
          <el-descriptions-item label="最后使用">{{ formatDateTime(selectedApiKey.last_used_at) }}</el-descriptions-item>
          <el-descriptions-item label="使用次数">{{ selectedApiKey.usage_count }}</el-descriptions-item>
          <el-descriptions-item label="描述" span="2">{{ selectedApiKey.description || '无' }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <template #footer>
        <el-button @click="showApiKeyDetail = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Connection, Message, ChatDotRound, Setting, Refresh
} from '@element-plus/icons-vue'

// 响应式数据
const showCreateApiKey = ref(false)
const showApiKeyDetail = ref(false)
const selectedApiKey = ref(null)
const creating = ref(false)

// 保存状态
const saving = reactive({
  shihuatong: false,
  email: false,
  sms: false
})

// 测试状态
const testing = reactive({
  shihuatong: false,
  email: false,
  sms: false
})

// 石化通配置
const shihuatongConfig = reactive({
  enabled: true,
  server_url: 'https://shihuatong.example.com',
  app_id: 'todo_system_001',
  app_secret: '',
  enable_push: true,
  sync_users: false
})

// 邮件配置
const emailConfig = reactive({
  enabled: true,
  smtp_host: 'smtp.qq.com',
  smtp_port: 587,
  smtp_user: '',
  smtp_password: '',
  from_name: '海南炼化Todo系统',
  from_email: 'noreply@hnlh.com',
  encryption: 'tls'
})

// 短信配置
const smsConfig = reactive({
  enabled: false,
  provider: 'aliyun',
  access_key: '',
  secret_key: '',
  sign_name: '海南炼化',
  template_id: ''
})

// API密钥列表
const apiKeys = ref([
  {
    id: 1,
    name: 'Web应用密钥',
    description: '用于Web应用的API访问',
    key: 'sk_test_1234567890abcdef',
    status: 'active',
    permissions: ['read', 'write'],
    created_at: '2024-01-01T00:00:00Z',
    expires_at: '2024-12-31T23:59:59Z',
    last_used_at: '2024-01-15T10:30:00Z',
    usage_count: 1250
  },
  {
    id: 2,
    name: '移动应用密钥',
    description: '用于移动应用的只读访问',
    key: 'sk_test_abcdef1234567890',
    status: 'active',
    permissions: ['read'],
    created_at: '2024-01-05T00:00:00Z',
    expires_at: null,
    last_used_at: '2024-01-14T16:20:00Z',
    usage_count: 856
  },
  {
    id: 3,
    name: '测试密钥',
    description: '用于开发测试',
    key: 'sk_test_fedcba0987654321',
    status: 'disabled',
    permissions: ['read', 'write', 'admin'],
    created_at: '2023-12-01T00:00:00Z',
    expires_at: '2024-06-01T00:00:00Z',
    last_used_at: '2024-01-10T09:15:00Z',
    usage_count: 342
  }
])

// 新API密钥表单
const newApiKey = reactive({
  name: '',
  description: '',
  permissions: ['read'],
  expires_in: 365
})

// 使用统计
const usageStats = reactive({
  email_today: 45,
  sms_today: 12,
  api_calls: 2856,
  shihuatong_push: 78
})

// 最近日志
const recentLogs = ref([
  {
    id: 1,
    service: '邮件服务',
    level: 'success',
    message: '成功发送任务分配通知邮件',
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: 2,
    service: 'API接口',
    level: 'info',
    message: 'API密钥 Web应用密钥 被使用',
    created_at: '2024-01-15T10:25:00Z'
  },
  {
    id: 3,
    service: '石化通',
    level: 'success',
    message: '成功推送消息到石化通',
    created_at: '2024-01-15T10:20:00Z'
  },
  {
    id: 4,
    service: '短信服务',
    level: 'warning',
    message: '短信发送失败，余额不足',
    created_at: '2024-01-15T10:15:00Z'
  },
  {
    id: 5,
    service: '邮件服务',
    level: 'error',
    message: 'SMTP连接超时',
    created_at: '2024-01-15T10:10:00Z'
  }
])

// 方法
const handleShihuatongToggle = (enabled) => {
  if (!enabled) {
    // 清空敏感信息
    shihuatongConfig.app_secret = ''
  }
}

const handleEmailToggle = (enabled) => {
  if (!enabled) {
    // 清空敏感信息
    emailConfig.smtp_password = ''
  }
}

const handleSmsToggle = (enabled) => {
  if (!enabled) {
    // 清空敏感信息
    smsConfig.secret_key = ''
  }
}

const saveShihuatongConfig = async () => {
  try {
    saving.shihuatong = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('石化通配置保存成功')
  } catch (error) {
    console.error('保存石化通配置失败:', error)
    ElMessage.error('保存石化通配置失败')
  } finally {
    saving.shihuatong = false
  }
}

const saveEmailConfig = async () => {
  try {
    saving.email = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1200))

    ElMessage.success('邮件配置保存成功')
  } catch (error) {
    console.error('保存邮件配置失败:', error)
    ElMessage.error('保存邮件配置失败')
  } finally {
    saving.email = false
  }
}

const saveSmsConfig = async () => {
  try {
    saving.sms = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 900))

    ElMessage.success('短信配置保存成功')
  } catch (error) {
    console.error('保存短信配置失败:', error)
    ElMessage.error('保存短信配置失败')
  } finally {
    saving.sms = false
  }
}

const testShihuatongConnection = async () => {
  try {
    testing.shihuatong = true

    // 模拟测试连接
    await new Promise(resolve => setTimeout(resolve, 2000))

    ElMessage.success('石化通连接测试成功')
  } catch (error) {
    console.error('石化通连接测试失败:', error)
    ElMessage.error('石化通连接测试失败')
  } finally {
    testing.shihuatong = false
  }
}

const testEmailConnection = async () => {
  try {
    testing.email = true

    // 模拟发送测试邮件
    await new Promise(resolve => setTimeout(resolve, 3000))

    ElMessage.success('测试邮件发送成功，请查收')
  } catch (error) {
    console.error('发送测试邮件失败:', error)
    ElMessage.error('发送测试邮件失败')
  } finally {
    testing.email = false
  }
}

const testSmsConnection = async () => {
  try {
    testing.sms = true

    // 模拟发送测试短信
    await new Promise(resolve => setTimeout(resolve, 2500))

    ElMessage.success('测试短信发送成功')
  } catch (error) {
    console.error('发送测试短信失败:', error)
    ElMessage.error('发送测试短信失败')
  } finally {
    testing.sms = false
  }
}

const createApiKey = async () => {
  try {
    if (!newApiKey.name.trim()) {
      ElMessage.warning('请输入密钥名称')
      return
    }

    creating.value = true

    // 模拟创建API密钥
    await new Promise(resolve => setTimeout(resolve, 1500))

    const newKey = {
      id: Date.now(),
      name: newApiKey.name,
      description: newApiKey.description,
      key: `sk_${Math.random().toString(36).substr(2, 20)}`,
      status: 'active',
      permissions: [...newApiKey.permissions],
      created_at: new Date().toISOString(),
      expires_at: newApiKey.expires_in > 0
        ? new Date(Date.now() + newApiKey.expires_in * 24 * 60 * 60 * 1000).toISOString()
        : null,
      last_used_at: null,
      usage_count: 0
    }

    apiKeys.value.unshift(newKey)

    // 重置表单
    Object.assign(newApiKey, {
      name: '',
      description: '',
      permissions: ['read'],
      expires_in: 365
    })

    showCreateApiKey.value = false
    ElMessage.success('API密钥创建成功')
  } catch (error) {
    console.error('创建API密钥失败:', error)
    ElMessage.error('创建API密钥失败')
  } finally {
    creating.value = false
  }
}

const viewApiKey = (apiKey) => {
  selectedApiKey.value = apiKey
  showApiKeyDetail.value = true
}

const toggleApiKey = async (apiKey) => {
  try {
    const action = apiKey.status === 'active' ? '禁用' : '启用'

    await ElMessageBox.confirm(
      `确定要${action}API密钥"${apiKey.name}"吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    apiKey.status = apiKey.status === 'active' ? 'disabled' : 'active'
    ElMessage.success(`API密钥${action}成功`)
  } catch {
    // 用户取消操作
  }
}

const deleteApiKey = async (apiKey) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除API密钥"${apiKey.name}"吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    const index = apiKeys.value.findIndex(k => k.id === apiKey.id)
    if (index > -1) {
      apiKeys.value.splice(index, 1)
    }

    ElMessage.success('API密钥删除成功')
  } catch {
    // 用户取消删除
  }
}

const copyApiKey = async (key) => {
  try {
    await navigator.clipboard.writeText(key)
    ElMessage.success('API密钥已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}

const refreshLogs = async () => {
  try {
    // 模拟刷新日志
    await new Promise(resolve => setTimeout(resolve, 500))

    // 添加一条新日志
    const newLog = {
      id: Date.now(),
      service: '系统',
      level: 'info',
      message: '日志已刷新',
      created_at: new Date().toISOString()
    }

    recentLogs.value.unshift(newLog)

    // 保持最多10条日志
    if (recentLogs.value.length > 10) {
      recentLogs.value = recentLogs.value.slice(0, 10)
    }

    ElMessage.success('日志已刷新')
  } catch (error) {
    console.error('刷新日志失败:', error)
    ElMessage.error('刷新日志失败')
  }
}

// 工具方法
const getPermissionText = (permission) => {
  const permissionMap = {
    read: '只读权限',
    write: '写入权限',
    admin: '管理权限'
  }
  return permissionMap[permission] || permission
}

const formatDate = (dateString) => {
  if (!dateString) return '从未'

  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDateTime = (dateString) => {
  if (!dateString) return '从未'

  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date

  // 小于1分钟
  if (diff < 60000) {
    return '刚刚'
  }

  // 小于1小时
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  }

  // 小于1天
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  }

  // 超过1天显示具体时间
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadIntegrationSettings = async () => {
  try {
    // 模拟加载集成设置
    await new Promise(resolve => setTimeout(resolve, 500))

    console.log('集成设置加载完成')
  } catch (error) {
    console.error('加载集成设置失败:', error)
    ElMessage.error('加载集成设置失败')
  }
}

// 生命周期
onMounted(() => {
  loadIntegrationSettings()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理对话框状态
  showCreateApiKey.value = false
  showApiKeyDetail.value = false
  selectedApiKey.value = null
})
</script>

<style scoped>
.integrations {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

/* 卡片样式 */
.integration-card,
.status-card,
.stats-card,
.logs-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1f2937;
}

/* 集成信息 */
.integration-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.integration-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.integration-icon.shihuatong {
  background: linear-gradient(135deg, #1890ff, #096dd9);
}

.integration-icon.email {
  background: linear-gradient(135deg, #52c41a, #389e0d);
}

.integration-icon.sms {
  background: linear-gradient(135deg, #fa8c16, #d46b08);
}

.integration-icon.api {
  background: linear-gradient(135deg, #722ed1, #531dab);
}

.integration-title {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.integration-description {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.integration-status {
  flex-shrink: 0;
}

/* 集成内容 */
.integration-content {
  padding: 8px 0;
}

.integration-form {
  margin-bottom: 20px;
}

.form-tip {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
  line-height: 1.4;
}

.integration-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

/* API密钥列表 */
.api-keys-list {
  padding: 8px 0;
}

.api-key-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px 0;
  border-bottom: 1px solid #f1f5f9;
}

.api-key-item:last-child {
  border-bottom: none;
}

.api-key-info {
  flex: 1;
  min-width: 0;
}

.api-key-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.api-key-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.api-key-details {
  margin-top: 8px;
}

.api-key-description {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #4b5563;
}

.api-key-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #6b7280;
}

.api-key-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.empty-api-keys {
  text-align: center;
  padding: 40px 20px;
}

/* 状态面板 */
.status-panel {
  position: sticky;
  top: 24px;
}

.status-list {
  padding: 8px 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.status-item:last-child {
  border-bottom: none;
}

.status-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: white;
}

.status-icon.shihuatong {
  background: #1890ff;
}

.status-icon.email {
  background: #52c41a;
}

.status-icon.sms {
  background: #fa8c16;
}

.status-icon.api {
  background: #722ed1;
}

.status-name {
  font-size: 14px;
  color: #1f2937;
  font-weight: 500;
}

.status-indicator {
  flex-shrink: 0;
}

/* 统计信息 */
.stats-list {
  padding: 8px 0;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.stats-item:last-child {
  border-bottom: none;
}

.stats-label {
  font-size: 14px;
  color: #4b5563;
}

.stats-value {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

/* 日志列表 */
.logs-list {
  padding: 8px 0;
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.log-item:last-child {
  border-bottom: none;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.log-service {
  font-size: 12px;
  font-weight: 600;
  color: #4b5563;
}

.log-time {
  font-size: 11px;
  color: #9ca3af;
}

.log-message {
  font-size: 13px;
  color: #1f2937;
  line-height: 1.4;
}

.log-item.success .log-service {
  color: #059669;
}

.log-item.warning .log-service {
  color: #d97706;
}

.log-item.error .log-service {
  color: #dc2626;
}

.log-item.info .log-service {
  color: #2563eb;
}

.empty-logs {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-size: 14px;
}

/* API密钥详情 */
.api-key-detail {
  padding: 8px 0;
}

.api-key-value {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .integrations {
    padding: 16px;
  }

  .integration-panels {
    margin-bottom: 24px;
  }

  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .integration-info {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .integration-actions {
    flex-direction: column;
  }

  .api-key-item {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .api-key-actions {
    justify-content: flex-end;
  }

  .api-key-meta {
    flex-direction: column;
    gap: 4px;
  }

  .status-item,
  .stats-item {
    padding: 16px 0;
  }
}

/* 表单项优化 */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

:deep(.el-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 对话框优化 */
:deep(.el-dialog__header) {
  padding: 20px 20px 10px;
}

:deep(.el-dialog__body) {
  padding: 10px 20px 20px;
}

/* 按钮样式 */
:deep(.el-button--small) {
  padding: 6px 12px;
  font-size: 13px;
}

/* 标签样式 */
:deep(.el-tag--small) {
  font-size: 11px;
  padding: 2px 6px;
}

/* 描述列表优化 */
:deep(.el-descriptions__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-descriptions__content) {
  color: #1f2937;
}
</style>
