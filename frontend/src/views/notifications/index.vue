<template>
  <div class="notifications">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><Bell /></el-icon>
            通知中心
          </h1>
          <p class="page-subtitle">查看和管理您的系统通知</p>
        </div>
        <div class="header-right">
          <el-button
            type="primary"
            @click="handleMarkAllRead"
            :disabled="!hasUnreadNotifications"
            size="large"
          >
            <el-icon><Check /></el-icon>
            全部标记已读
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon unread">
                <el-icon><Message /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.unread_count || 0 }}</div>
                <div class="stats-label">未读通知</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon total">
                <el-icon><Bell /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.total_count || 0 }}</div>
                <div class="stats-label">总通知数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon today">
                <el-icon><Calendar /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.today_count || 0 }}</div>
                <div class="stats-label">今日通知</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon system">
                <el-icon><Setting /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.system_count || 0 }}</div>
                <div class="stats-label">系统通知</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧通知列表 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <el-card class="notifications-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>通知列表</span>
                <div class="header-actions">
                  <el-select v-model="filters.type" placeholder="通知类型" style="width: 120px; margin-right: 12px" clearable>
                    <el-option label="全部类型" value="" />
                    <el-option label="系统通知" value="system" />
                    <el-option label="任务通知" value="task" />
                    <el-option label="审批通知" value="approval" />
                    <el-option label="提醒通知" value="reminder" />
                  </el-select>
                  <el-select v-model="filters.is_read" placeholder="阅读状态" style="width: 120px; margin-right: 12px" clearable>
                    <el-option label="全部状态" :value="null" />
                    <el-option label="未读" :value="false" />
                    <el-option label="已读" :value="true" />
                  </el-select>
                  <el-button @click="handleRefresh" :loading="loading">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>

            <!-- 批量操作 -->
            <div v-if="selectedNotifications.length > 0" class="batch-actions">
              <el-alert
                :title="`已选择 ${selectedNotifications.length} 条通知`"
                type="info"
                show-icon
                :closable="false"
              >
                <template #default>
                  <div class="batch-buttons">
                    <el-button size="small" @click="handleBatchMarkRead">
                      <el-icon><Check /></el-icon>
                      标记已读
                    </el-button>
                    <el-button size="small" type="danger" @click="handleBatchDelete">
                      <el-icon><Delete /></el-icon>
                      批量删除
                    </el-button>
                    <el-button size="small" @click="selectedNotifications = []">
                      取消选择
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>

            <!-- 通知列表 -->
            <div v-loading="loading" class="notifications-list">
              <div v-if="notifications.length === 0" class="empty-state">
                <el-empty description="暂无通知" />
              </div>
              <div v-else>
                <div
                  v-for="notification in notifications"
                  v-if="notification && notification.id"
                  :key="`notification-${notification.id}`"
                  class="notification-item"
                  :class="{ 'unread': !notification.is_read, 'selected': selectedNotifications.includes(notification.id) }"
                  @click="handleNotificationClick(notification)"
                >
                  <div class="notification-checkbox">
                    <el-checkbox
                      v-model="selectedNotifications"
                      :value="notification.id"
                      @click.stop
                    />
                  </div>
                  <div class="notification-icon">
                    <el-icon v-if="notification.type === 'system'" class="system-icon"><Setting /></el-icon>
                    <el-icon v-else-if="notification.type === 'task'" class="task-icon"><Document /></el-icon>
                    <el-icon v-else-if="notification.type === 'approval'" class="approval-icon"><CircleCheck /></el-icon>
                    <el-icon v-else class="default-icon"><Bell /></el-icon>
                  </div>
                  <div class="notification-content">
                    <div class="notification-header">
                      <h4 class="notification-title">{{ notification.title }}</h4>
                      <div class="notification-meta">
                        <el-tag :type="getNotificationTypeColor(notification.type)" size="small">
                          {{ getNotificationTypeText(notification.type) }}
                        </el-tag>
                        <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                      </div>
                    </div>
                    <p class="notification-summary">{{ notification.content }}</p>
                  </div>
                  <div class="notification-actions">
                    <el-button
                      v-if="!notification.is_read"
                      size="small"
                      @click.stop="handleMarkRead(notification)"
                    >
                      标记已读
                    </el-button>
                    <el-button
                      size="small"
                      type="danger"
                      @click.stop="handleDelete(notification)"
                    >
                      删除
                    </el-button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分页 -->
            <div v-if="total > 0" class="pagination-wrapper">
              <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.page_size"
                :total="total"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 右侧通知详情 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <el-card class="detail-card" shadow="never">
            <template #header>
              <span>通知详情</span>
            </template>

            <div v-if="!selectedNotification" class="no-selection">
              <el-empty description="请选择一条通知查看详情" />
            </div>

            <div v-else class="notification-detail">
              <div class="detail-header">
                <h3 class="detail-title">{{ selectedNotification.title }}</h3>
                <div class="detail-meta">
                  <el-tag :type="getNotificationTypeColor(selectedNotification.type)">
                    {{ getNotificationTypeText(selectedNotification.type) }}
                  </el-tag>
                  <el-tag v-if="!selectedNotification.is_read" type="warning">未读</el-tag>
                  <el-tag v-else type="success">已读</el-tag>
                </div>
              </div>

              <div class="detail-content">
                <div class="detail-section">
                  <h4>通知内容</h4>
                  <div class="content-text" v-html="selectedNotification.content"></div>
                </div>

                <div class="detail-section">
                  <h4>通知信息</h4>
                  <div class="info-list">
                    <div class="info-item">
                      <span class="info-label">发送时间：</span>
                      <span class="info-value">{{ formatDateTime(selectedNotification.created_at) }}</span>
                    </div>
                    <div v-if="selectedNotification.sender" class="info-item">
                      <span class="info-label">发送人：</span>
                      <span class="info-value">{{ selectedNotification.sender.real_name }}</span>
                    </div>
                    <div v-if="selectedNotification.read_at" class="info-item">
                      <span class="info-label">阅读时间：</span>
                      <span class="info-value">{{ formatDateTime(selectedNotification.read_at) }}</span>
                    </div>
                  </div>
                </div>

                <div v-if="selectedNotification.related_url" class="detail-section">
                  <h4>相关链接</h4>
                  <el-button type="primary" @click="handleGoToRelated(selectedNotification)">
                    查看相关内容
                  </el-button>
                </div>
              </div>

              <div class="detail-actions">
                <el-button
                  v-if="!selectedNotification.is_read"
                  type="primary"
                  @click="handleMarkRead(selectedNotification)"
                >
                  标记已读
                </el-button>
                <el-button
                  type="danger"
                  @click="handleDelete(selectedNotification)"
                >
                  删除通知
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Bell, Check, Message, Calendar, Setting, Refresh, Delete,
  Document, CircleCheck
} from '@element-plus/icons-vue'
import {
  getNotifications,
  getNotificationStats,
  markAsRead,
  batchMarkAsRead,
  markAllAsRead,
  deleteNotification,
  batchDeleteNotifications
} from '@/api/notifications'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const notifications = ref([])
const selectedNotification = ref(null)
const selectedNotifications = ref([])
const total = ref(0)
const stats = ref({})

// 分页参数
const pagination = reactive({
  page: 1,
  page_size: 20
})

// 筛选参数
const filters = reactive({
  type: '',
  is_read: null
})

// 计算属性
const hasUnreadNotifications = computed(() => {
  return notifications.value.some(n => !n.is_read)
})

// 模拟数据
const mockNotifications = [
  {
    id: 1,
    title: '新任务分配通知',
    content: '您有一个新的任务"完成项目需求分析"已分配给您，请及时查看并处理。',
    type: 'task',
    is_read: false,
    created_at: '2024-01-15T10:30:00Z',
    read_at: null,
    sender: { real_name: '张经理' },
    related_url: '/tasks/1'
  },
  {
    id: 2,
    title: '系统维护通知',
    content: '系统将于今晚22:00-24:00进行维护升级，期间可能影响正常使用，请提前保存工作内容。',
    type: 'system',
    is_read: true,
    created_at: '2024-01-14T16:00:00Z',
    read_at: '2024-01-14T16:30:00Z',
    sender: { real_name: '系统管理员' },
    related_url: null
  },
  {
    id: 3,
    title: '任务审批通过',
    content: '您提交的任务"技术方案设计"已通过审批，可以开始执行。',
    type: 'approval',
    is_read: false,
    created_at: '2024-01-14T14:20:00Z',
    read_at: null,
    sender: { real_name: '李主任' },
    related_url: '/tasks/2'
  },
  {
    id: 4,
    title: '任务即将到期提醒',
    content: '您的任务"项目进度汇报"将于明天到期，请及时完成。',
    type: 'reminder',
    is_read: false,
    created_at: '2024-01-13T09:00:00Z',
    read_at: null,
    sender: null,
    related_url: '/tasks/3'
  },
  {
    id: 5,
    title: '部门会议通知',
    content: '技术部将于本周五下午2点召开月度工作会议，请准时参加。',
    type: 'system',
    is_read: true,
    created_at: '2024-01-12T11:00:00Z',
    read_at: '2024-01-12T11:15:00Z',
    sender: { real_name: '人事部' },
    related_url: null
  }
]

const mockStats = {
  unread_count: 3,
  total_count: 15,
  today_count: 2,
  system_count: 8
}

// 方法
const loadData = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 应用筛选
    let filteredNotifications = [...mockNotifications]

    if (filters.type) {
      filteredNotifications = filteredNotifications.filter(n => n.type === filters.type)
    }

    if (filters.is_read !== null) {
      filteredNotifications = filteredNotifications.filter(n => n.is_read === filters.is_read)
    }

    // 分页
    const start = (pagination.page - 1) * pagination.page_size
    const end = start + pagination.page_size

    notifications.value = filteredNotifications.slice(start, end)
    total.value = filteredNotifications.length

    // 如果有选中的通知，更新详情
    if (selectedNotification.value) {
      const updated = notifications.value.find(n => n.id === selectedNotification.value.id)
      if (updated) {
        selectedNotification.value = updated
      }
    }
  } catch (error) {
    console.error('加载通知失败:', error)
    ElMessage.error('加载通知失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 200))
    stats.value = mockStats
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

// 通知点击处理
const handleNotificationClick = (notification) => {
  selectedNotification.value = notification

  // 如果是未读通知，自动标记为已读
  if (!notification.is_read) {
    handleMarkRead(notification, false)
  }
}

// 标记单个通知为已读
const handleMarkRead = async (notification, showMessage = true) => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 200))

    // 更新本地数据
    notification.is_read = true
    notification.read_at = new Date().toISOString()

    // 更新统计
    stats.value.unread_count = Math.max(0, stats.value.unread_count - 1)

    if (showMessage) {
      ElMessage.success('已标记为已读')
    }
  } catch (error) {
    console.error('标记已读失败:', error)
    ElMessage.error('标记已读失败')
  }
}

// 批量标记已读
const handleBatchMarkRead = async () => {
  if (selectedNotifications.value.length === 0) {
    ElMessage.warning('请先选择要标记的通知')
    return
  }

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    // 更新本地数据
    selectedNotifications.value.forEach(id => {
      const notification = notifications.value.find(n => n.id === id)
      if (notification && !notification.is_read) {
        notification.is_read = true
        notification.read_at = new Date().toISOString()
        stats.value.unread_count = Math.max(0, stats.value.unread_count - 1)
      }
    })

    selectedNotifications.value = []
    ElMessage.success('批量标记已读成功')
  } catch (error) {
    console.error('批量标记已读失败:', error)
    ElMessage.error('批量标记已读失败')
  }
}

// 全部标记已读
const handleMarkAllRead = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要将所有未读通知标记为已读吗？',
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 更新本地数据
    notifications.value.forEach(notification => {
      if (!notification.is_read) {
        notification.is_read = true
        notification.read_at = new Date().toISOString()
      }
    })

    stats.value.unread_count = 0
    ElMessage.success('所有通知已标记为已读')
  } catch {
    // 用户取消操作
  }
}

// 删除单个通知
const handleDelete = async (notification) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除通知"${notification.title}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    // 更新本地数据
    const index = notifications.value.findIndex(n => n.id === notification.id)
    if (index > -1) {
      notifications.value.splice(index, 1)
      total.value--

      if (!notification.is_read) {
        stats.value.unread_count = Math.max(0, stats.value.unread_count - 1)
      }
      stats.value.total_count = Math.max(0, stats.value.total_count - 1)
    }

    // 如果删除的是当前选中的通知，清空选择
    if (selectedNotification.value && selectedNotification.value.id === notification.id) {
      selectedNotification.value = null
    }

    ElMessage.success('通知删除成功')
  } catch {
    // 用户取消删除
  }
}

// 批量删除通知
const handleBatchDelete = async () => {
  if (selectedNotifications.value.length === 0) {
    ElMessage.warning('请先选择要删除的通知')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedNotifications.value.length} 条通知吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 更新本地数据
    let deletedUnreadCount = 0
    selectedNotifications.value.forEach(id => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index > -1) {
        const notification = notifications.value[index]
        if (!notification.is_read) {
          deletedUnreadCount++
        }
        notifications.value.splice(index, 1)
      }
    })

    total.value -= selectedNotifications.value.length
    stats.value.unread_count = Math.max(0, stats.value.unread_count - deletedUnreadCount)
    stats.value.total_count = Math.max(0, stats.value.total_count - selectedNotifications.value.length)

    // 如果删除的包含当前选中的通知，清空选择
    if (selectedNotification.value && selectedNotifications.value.includes(selectedNotification.value.id)) {
      selectedNotification.value = null
    }

    selectedNotifications.value = []
    ElMessage.success('批量删除成功')
  } catch {
    // 用户取消删除
  }
}

// 刷新数据
const handleRefresh = () => {
  loadData()
  loadStats()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadData()
}

// 跳转到相关内容
const handleGoToRelated = (notification) => {
  if (notification.related_url) {
    router.push(notification.related_url)
  }
}

// 工具方法
const getNotificationTypeText = (type) => {
  const typeMap = {
    system: '系统通知',
    task: '任务通知',
    approval: '审批通知',
    reminder: '提醒通知'
  }
  return typeMap[type] || '其他通知'
}

const getNotificationTypeColor = (type) => {
  const colorMap = {
    system: 'info',
    task: 'primary',
    approval: 'success',
    reminder: 'warning'
  }
  return colorMap[type] || 'default'
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

  // 小于7天
  if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  }

  // 超过7天显示具体日期
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 监听筛选条件变化
watch([() => filters.type, () => filters.is_read], () => {
  pagination.page = 1
  loadData()
}, { deep: true })

// 生命周期
onMounted(() => {
  loadData()
  loadStats()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理选中状态
  selectedNotifications.value = []
  selectedNotification.value = null
})
</script>

<style scoped>
.notifications {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left .page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
}

.header-left .page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

/* 统计卡片 */
.stats-cards {
  margin-bottom: 24px;
}

.stats-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.stats-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stats-icon.unread {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stats-icon.total {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.stats-icon.today {
  background: linear-gradient(135deg, #10b981, #047857);
}

.stats-icon.system {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stats-label {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

/* 主要内容 */
.main-content {
  margin-bottom: 24px;
}

.notifications-card,
.detail-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1f2937;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 批量操作 */
.batch-actions {
  margin-bottom: 16px;
}

.batch-buttons {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

/* 通知列表 */
.notifications-list {
  min-height: 400px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.notification-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.notification-item.unread {
  border-left: 4px solid #3b82f6;
  background: #f8faff;
}

.notification-item.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.notification-checkbox {
  margin-top: 2px;
}

.notification-icon {
  margin-top: 2px;
  font-size: 20px;
}

.notification-icon .system-icon {
  color: #8b5cf6;
}

.notification-icon .task-icon {
  color: #3b82f6;
}

.notification-icon .approval-icon {
  color: #10b981;
}

.notification-icon .default-icon {
  color: #6b7280;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notification-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.4;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.notification-time {
  font-size: 12px;
  color: #6b7280;
  white-space: nowrap;
}

.notification-summary {
  margin: 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-left: 8px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 通知详情 */
.no-selection {
  text-align: center;
  padding: 40px 20px;
}

.notification-detail {
  padding: 4px 0;
}

.detail-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.4;
}

.detail-meta {
  display: flex;
  gap: 8px;
}

.detail-content {
  margin-bottom: 24px;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.content-text {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
  border-left: 3px solid #3b82f6;
}

.info-list {
  space-y: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.info-value {
  font-size: 13px;
  color: #1f2937;
  text-align: right;
}

.detail-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .notifications {
    padding: 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .header-actions {
    flex-wrap: wrap;
  }

  .notification-item {
    flex-direction: column;
    gap: 8px;
  }

  .notification-header {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }

  .notification-actions {
    flex-direction: row;
    justify-content: flex-end;
  }

  .detail-actions {
    flex-direction: column;
  }

  .batch-buttons {
    flex-wrap: wrap;
  }
}
</style>
