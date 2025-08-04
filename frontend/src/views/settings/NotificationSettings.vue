<template>
  <div class="notification-settings">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Bell /></el-icon>
        通知设置
      </h1>
      <p class="page-subtitle">管理您的通知偏好和接收方式</p>
    </div>

    <div class="settings-content">
      <el-row :gutter="24">
        <!-- 左侧设置面板 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <div class="settings-panels">
            <!-- 通知类型设置 -->
            <el-card class="settings-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>通知类型设置</span>
                  <el-button
                    type="primary"
                    @click="saveNotificationTypes"
                    :loading="saving.types"
                    size="small"
                  >
                    保存设置
                  </el-button>
                </div>
              </template>

              <div class="notification-types">
                <div
                  v-for="type in notificationTypes"
                  :key="type.key"
                  class="notification-type-item"
                >
                  <div class="type-info">
                    <div class="type-header">
                      <el-icon :class="type.iconClass">
                        <component :is="type.icon" />
                      </el-icon>
                      <h4 class="type-title">{{ type.title }}</h4>
                    </div>
                    <p class="type-description">{{ type.description }}</p>
                  </div>

                  <div class="type-controls">
                    <div class="control-group">
                      <label class="control-label">邮件通知</label>
                      <el-switch
                        v-model="notificationSettings[type.key].email"
                        @change="handleSettingChange"
                      />
                    </div>
                    <div class="control-group">
                      <label class="control-label">短信通知</label>
                      <el-switch
                        v-model="notificationSettings[type.key].sms"
                        @change="handleSettingChange"
                      />
                    </div>
                    <div class="control-group">
                      <label class="control-label">系统通知</label>
                      <el-switch
                        v-model="notificationSettings[type.key].system"
                        @change="handleSettingChange"
                      />
                    </div>
                    <div class="control-group">
                      <label class="control-label">桌面通知</label>
                      <el-switch
                        v-model="notificationSettings[type.key].desktop"
                        @change="handleSettingChange"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 通知时间设置 -->
            <el-card class="settings-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>通知时间设置</span>
                  <el-button
                    type="primary"
                    @click="saveTimeSettings"
                    :loading="saving.time"
                    size="small"
                  >
                    保存设置
                  </el-button>
                </div>
              </template>

              <el-form :model="timeSettings" label-width="120px" class="time-form">
                <el-form-item label="免打扰时间">
                  <div class="time-range-group">
                    <el-time-picker
                      v-model="timeSettings.quiet_start"
                      placeholder="开始时间"
                      format="HH:mm"
                      value-format="HH:mm"
                    />
                    <span class="time-separator">至</span>
                    <el-time-picker
                      v-model="timeSettings.quiet_end"
                      placeholder="结束时间"
                      format="HH:mm"
                      value-format="HH:mm"
                    />
                  </div>
                  <div class="form-tip">在此时间段内不会发送通知</div>
                </el-form-item>

                <el-form-item label="工作日通知">
                  <el-checkbox-group v-model="timeSettings.work_days">
                    <el-checkbox value="1">周一</el-checkbox>
                    <el-checkbox value="2">周二</el-checkbox>
                    <el-checkbox value="3">周三</el-checkbox>
                    <el-checkbox value="4">周四</el-checkbox>
                    <el-checkbox value="5">周五</el-checkbox>
                    <el-checkbox value="6">周六</el-checkbox>
                    <el-checkbox value="0">周日</el-checkbox>
                  </el-checkbox-group>
                  <div class="form-tip">只在选中的工作日发送通知</div>
                </el-form-item>

                <el-form-item label="通知频率">
                  <el-radio-group v-model="timeSettings.frequency">
                    <el-radio value="immediate">立即通知</el-radio>
                    <el-radio value="hourly">每小时汇总</el-radio>
                    <el-radio value="daily">每日汇总</el-radio>
                  </el-radio-group>
                  <div class="form-tip">选择通知的发送频率</div>
                </el-form-item>
              </el-form>
            </el-card>

            <!-- 邮件设置 -->
            <el-card class="settings-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>邮件设置</span>
                  <el-button
                    type="primary"
                    @click="saveEmailSettings"
                    :loading="saving.email"
                    size="small"
                  >
                    保存设置
                  </el-button>
                </div>
              </template>

              <el-form :model="emailSettings" label-width="120px" class="email-form">
                <el-form-item label="邮件地址">
                  <el-input
                    v-model="emailSettings.email"
                    placeholder="请输入邮件地址"
                    disabled
                  />
                  <div class="form-tip">邮件地址来自个人资料设置</div>
                </el-form-item>

                <el-form-item label="邮件格式">
                  <el-radio-group v-model="emailSettings.format">
                    <el-radio value="html">HTML格式</el-radio>
                    <el-radio value="text">纯文本格式</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="邮件语言">
                  <el-select v-model="emailSettings.language" style="width: 200px">
                    <el-option label="简体中文" value="zh-CN" />
                    <el-option label="English" value="en-US" />
                  </el-select>
                </el-form-item>

                <el-form-item label="包含附件">
                  <el-checkbox v-model="emailSettings.include_attachments">
                    在邮件中包含相关附件
                  </el-checkbox>
                </el-form-item>

                <el-form-item label="邮件签名">
                  <el-input
                    v-model="emailSettings.signature"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入邮件签名"
                  />
                </el-form-item>
              </el-form>
            </el-card>

            <!-- 短信设置 -->
            <el-card class="settings-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>短信设置</span>
                  <el-button
                    type="primary"
                    @click="saveSmsSettings"
                    :loading="saving.sms"
                    size="small"
                  >
                    保存设置
                  </el-button>
                </div>
              </template>

              <el-form :model="smsSettings" label-width="120px" class="sms-form">
                <el-form-item label="手机号码">
                  <el-input
                    v-model="smsSettings.phone"
                    placeholder="请输入手机号码"
                    disabled
                  />
                  <div class="form-tip">手机号码来自个人资料设置</div>
                </el-form-item>

                <el-form-item label="短信模板">
                  <el-select v-model="smsSettings.template" style="width: 200px">
                    <el-option label="简洁模板" value="simple" />
                    <el-option label="详细模板" value="detailed" />
                  </el-select>
                </el-form-item>

                <el-form-item label="紧急通知">
                  <el-checkbox v-model="smsSettings.urgent_only">
                    只接收紧急通知短信
                  </el-checkbox>
                  <div class="form-tip">开启后只有高优先级任务才会发送短信</div>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
        </el-col>

        <!-- 右侧预览和测试 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <div class="preview-panel">
            <!-- 通知预览 -->
            <el-card class="preview-card" shadow="never">
              <template #header>
                <span>通知预览</span>
              </template>

              <div class="preview-content">
                <div class="preview-tabs">
                  <el-tabs v-model="previewType" @tab-change="updatePreview">
                    <el-tab-pane label="邮件" name="email">
                      <div class="email-preview">
                        <div class="email-header">
                          <div class="email-subject">{{ emailPreview.subject }}</div>
                          <div class="email-from">来自：{{ emailPreview.from }}</div>
                        </div>
                        <div class="email-body" v-html="emailPreview.body"></div>
                      </div>
                    </el-tab-pane>
                    <el-tab-pane label="短信" name="sms">
                      <div class="sms-preview">
                        <div class="sms-phone">发送至：{{ smsPreview.phone }}</div>
                        <div class="sms-content">{{ smsPreview.content }}</div>
                      </div>
                    </el-tab-pane>
                    <el-tab-pane label="系统" name="system">
                      <div class="system-preview">
                        <div class="notification-item preview">
                          <div class="notification-icon">
                            <el-icon><Bell /></el-icon>
                          </div>
                          <div class="notification-content">
                            <div class="notification-title">{{ systemPreview.title }}</div>
                            <div class="notification-message">{{ systemPreview.message }}</div>
                            <div class="notification-time">{{ systemPreview.time }}</div>
                          </div>
                        </div>
                      </div>
                    </el-tab-pane>
                  </el-tabs>
                </div>
              </div>
            </el-card>

            <!-- 测试通知 -->
            <el-card class="test-card" shadow="never">
              <template #header>
                <span>测试通知</span>
              </template>

              <div class="test-content">
                <p class="test-description">发送测试通知以验证您的设置</p>

                <div class="test-buttons">
                  <el-button
                    type="primary"
                    @click="sendTestNotification('email')"
                    :loading="testing.email"
                    block
                  >
                    <el-icon><Message /></el-icon>
                    发送测试邮件
                  </el-button>

                  <el-button
                    type="primary"
                    @click="sendTestNotification('sms')"
                    :loading="testing.sms"
                    block
                  >
                    <el-icon><ChatDotRound /></el-icon>
                    发送测试短信
                  </el-button>

                  <el-button
                    type="primary"
                    @click="sendTestNotification('system')"
                    :loading="testing.system"
                    block
                  >
                    <el-icon><Bell /></el-icon>
                    发送系统通知
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- 通知统计 -->
            <el-card class="stats-card" shadow="never">
              <template #header>
                <span>通知统计</span>
              </template>

              <div class="stats-content">
                <div class="stats-item">
                  <div class="stats-label">今日通知</div>
                  <div class="stats-value">{{ notificationStats.today }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">本周通知</div>
                  <div class="stats-value">{{ notificationStats.week }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">本月通知</div>
                  <div class="stats-value">{{ notificationStats.month }}</div>
                </div>
                <div class="stats-item">
                  <div class="stats-label">未读通知</div>
                  <div class="stats-value unread">{{ notificationStats.unread }}</div>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Bell, Message, ChatDotRound, Document, CircleCheck, Warning,
  Setting, Calendar, Clock
} from '@element-plus/icons-vue'

// 响应式数据
const previewType = ref('email')
const hasChanges = ref(false)

// 保存状态
const saving = reactive({
  types: false,
  time: false,
  email: false,
  sms: false
})

// 测试状态
const testing = reactive({
  email: false,
  sms: false,
  system: false
})

// 通知类型配置
const notificationTypes = [
  {
    key: 'task_assigned',
    title: '任务分配',
    description: '当有新任务分配给您时',
    icon: Document,
    iconClass: 'task-icon'
  },
  {
    key: 'task_completed',
    title: '任务完成',
    description: '当您的任务被标记为完成时',
    icon: CircleCheck,
    iconClass: 'completed-icon'
  },
  {
    key: 'task_overdue',
    title: '任务逾期',
    description: '当任务超过截止日期时',
    icon: Warning,
    iconClass: 'overdue-icon'
  },
  {
    key: 'task_reminder',
    title: '任务提醒',
    description: '任务截止日期前的提醒',
    icon: Clock,
    iconClass: 'reminder-icon'
  },
  {
    key: 'system_announcement',
    title: '系统公告',
    description: '系统维护和重要公告',
    icon: Setting,
    iconClass: 'system-icon'
  },
  {
    key: 'meeting_reminder',
    title: '会议提醒',
    description: '会议开始前的提醒通知',
    icon: Calendar,
    iconClass: 'meeting-icon'
  }
]

// 通知设置
const notificationSettings = reactive({
  task_assigned: {
    email: true,
    sms: false,
    system: true,
    desktop: true
  },
  task_completed: {
    email: true,
    sms: false,
    system: true,
    desktop: false
  },
  task_overdue: {
    email: true,
    sms: true,
    system: true,
    desktop: true
  },
  task_reminder: {
    email: true,
    sms: false,
    system: true,
    desktop: true
  },
  system_announcement: {
    email: true,
    sms: false,
    system: true,
    desktop: false
  },
  meeting_reminder: {
    email: true,
    sms: true,
    system: true,
    desktop: true
  }
})

// 时间设置
const timeSettings = reactive({
  quiet_start: '22:00',
  quiet_end: '08:00',
  work_days: ['1', '2', '3', '4', '5'],
  frequency: 'immediate'
})

// 邮件设置
const emailSettings = reactive({
  email: 'zhangsan@example.com',
  format: 'html',
  language: 'zh-CN',
  include_attachments: true,
  signature: '此邮件由海南炼化Todo系统自动发送，请勿回复。'
})

// 短信设置
const smsSettings = reactive({
  phone: '13800138000',
  template: 'simple',
  urgent_only: false
})

// 通知统计
const notificationStats = reactive({
  today: 8,
  week: 45,
  month: 156,
  unread: 12
})

// 预览数据
const emailPreview = computed(() => ({
  subject: '【海南炼化Todo】新任务分配通知',
  from: 'noreply@hnlh-todo.com',
  body: `
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <h2 style="color: #1f2937;">您有新的任务分配</h2>
      <p>尊敬的张三，</p>
      <p>您有一个新的任务已分配给您：</p>
      <div style="background: #f8fafc; padding: 16px; border-radius: 8px; margin: 16px 0;">
        <h3 style="margin: 0 0 8px 0; color: #3b82f6;">完成项目需求分析</h3>
        <p style="margin: 0; color: #6b7280;">截止日期：2024-01-20</p>
      </div>
      <p>请及时查看并处理。</p>
      <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">
      <p style="font-size: 12px; color: #9ca3af;">${emailSettings.signature}</p>
    </div>
  `
}))

const smsPreview = computed(() => ({
  phone: smsSettings.phone,
  content: smsSettings.template === 'simple'
    ? '【海南炼化Todo】您有新任务：完成项目需求分析，截止1月20日。'
    : '【海南炼化Todo】任务分配通知：您有新任务"完成项目需求分析"已分配，优先级：高，截止日期：2024年1月20日，请及时处理。'
}))

const systemPreview = computed(() => ({
  title: '新任务分配',
  message: '您有一个新的任务"完成项目需求分析"已分配给您',
  time: '刚刚'
}))

// 方法
const handleSettingChange = () => {
  hasChanges.value = true
}

const saveNotificationTypes = async () => {
  try {
    saving.types = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    hasChanges.value = false
    ElMessage.success('通知类型设置保存成功')
  } catch (error) {
    console.error('保存通知类型设置失败:', error)
    ElMessage.error('保存通知类型设置失败')
  } finally {
    saving.types = false
  }
}

const saveTimeSettings = async () => {
  try {
    saving.time = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))

    ElMessage.success('通知时间设置保存成功')
  } catch (error) {
    console.error('保存通知时间设置失败:', error)
    ElMessage.error('保存通知时间设置失败')
  } finally {
    saving.time = false
  }
}

const saveEmailSettings = async () => {
  try {
    saving.email = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 900))

    ElMessage.success('邮件设置保存成功')
  } catch (error) {
    console.error('保存邮件设置失败:', error)
    ElMessage.error('保存邮件设置失败')
  } finally {
    saving.email = false
  }
}

const saveSmsSettings = async () => {
  try {
    saving.sms = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 700))

    ElMessage.success('短信设置保存成功')
  } catch (error) {
    console.error('保存短信设置失败:', error)
    ElMessage.error('保存短信设置失败')
  } finally {
    saving.sms = false
  }
}

const sendTestNotification = async (type) => {
  try {
    testing[type] = true

    // 模拟发送测试通知
    await new Promise(resolve => setTimeout(resolve, 1500))

    const typeNames = {
      email: '测试邮件',
      sms: '测试短信',
      system: '系统通知'
    }

    ElMessage.success(`${typeNames[type]}发送成功，请查收`)
  } catch (error) {
    console.error(`发送${type}测试通知失败:`, error)
    ElMessage.error('发送测试通知失败')
  } finally {
    testing[type] = false
  }
}

const updatePreview = (tabName) => {
  previewType.value = tabName
}

const loadSettings = async () => {
  try {
    // 模拟加载设置数据
    await new Promise(resolve => setTimeout(resolve, 500))

    // 这里可以从API加载实际的设置数据
    console.log('设置数据加载完成')
  } catch (error) {
    console.error('加载设置失败:', error)
    ElMessage.error('加载设置失败')
  }
}

// 生命周期
onMounted(() => {
  loadSettings()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理状态
  hasChanges.value = false
})
</script>

<style scoped>
.notification-settings {
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
.settings-card,
.preview-card,
.test-card,
.stats-card {
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

/* 通知类型设置 */
.notification-types {
  padding: 8px 0;
}

.notification-type-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 20px 0;
  border-bottom: 1px solid #f1f5f9;
}

.notification-type-item:last-child {
  border-bottom: none;
}

.type-info {
  flex: 1;
  min-width: 0;
}

.type-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.type-header .el-icon {
  font-size: 20px;
}

.type-header .task-icon {
  color: #3b82f6;
}

.type-header .completed-icon {
  color: #10b981;
}

.type-header .overdue-icon {
  color: #ef4444;
}

.type-header .reminder-icon {
  color: #f59e0b;
}

.type-header .system-icon {
  color: #8b5cf6;
}

.type-header .meeting-icon {
  color: #06b6d4;
}

.type-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.type-description {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

.type-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 120px;
}

.control-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.control-label {
  font-size: 13px;
  color: #4b5563;
  font-weight: 500;
}

/* 表单样式 */
.time-form,
.email-form,
.sms-form {
  padding: 8px 0;
}

.time-range-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.time-separator {
  color: #6b7280;
  font-weight: 500;
}

.form-tip {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
  line-height: 1.4;
}

:deep(.el-checkbox-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 预览面板 */
.preview-panel {
  position: sticky;
  top: 24px;
}

.preview-content {
  padding: 8px 0;
}

.preview-tabs {
  min-height: 200px;
}

/* 邮件预览 */
.email-preview {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.email-header {
  background: #f8fafc;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.email-subject {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.email-from {
  font-size: 12px;
  color: #6b7280;
}

.email-body {
  padding: 16px;
  background: white;
  font-size: 14px;
  line-height: 1.6;
}

/* 短信预览 */
.sms-preview {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}

.sms-phone {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 8px;
}

.sms-content {
  font-size: 14px;
  color: #1f2937;
  line-height: 1.5;
}

/* 系统通知预览 */
.system-preview {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}

.notification-item.preview {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 0;
  border: none;
  background: white;
  border-radius: 6px;
  padding: 12px;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.notification-message {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 12px;
  color: #6b7280;
}

/* 测试通知 */
.test-content {
  padding: 8px 0;
}

.test-description {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #6b7280;
  text-align: center;
}

.test-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 统计信息 */
.stats-content {
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

.stats-value.unread {
  color: #ef4444;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .notification-settings {
    padding: 16px;
  }

  .settings-panels {
    margin-bottom: 24px;
  }

  .notification-type-item {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .type-controls {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 16px;
  }

  .control-group {
    flex-direction: column;
    gap: 4px;
    text-align: center;
  }

  .time-range-group {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }

  .card-header {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
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

:deep(.el-switch) {
  --el-switch-on-color: #3b82f6;
}

/* 标签页优化 */
:deep(.el-tabs__header) {
  margin-bottom: 16px;
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: #e5e7eb;
}

/* 按钮样式 */
:deep(.el-button--small) {
  padding: 6px 12px;
  font-size: 13px;
}
</style>
