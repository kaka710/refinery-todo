<template>
  <div class="dashboard-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">
          {{ getGreeting() }}，{{ userInfo?.real_name || '用户' }}！
        </h1>
        <p class="welcome-subtitle">
          今天是 {{ formatDate(new Date(), 'YYYY年MM月DD日 dddd') }}
        </p>
      </div>
      <div class="welcome-actions">
        <el-button 
          v-if="canCreateTask" 
          type="primary" 
          size="large" 
          @click="$router.push('/tasks/create')"
        >
          <el-icon><Plus /></el-icon>
          创建任务
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon pending">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.my_pending_tasks || 0 }}</div>
            <div class="stat-label">待处理任务</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon completed">
            <el-icon><Check /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.completed_tasks || 0 }}</div>
            <div class="stat-label">已完成任务</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon overdue">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.overdue_count || 0 }}</div>
            <div class="stat-label">逾期任务</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon total">
            <el-icon><List /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.total_tasks || 0 }}</div>
            <div class="stat-label">总任务数</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-left">
        <!-- 我的任务 -->
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">我的任务</h3>
            <el-button text @click="$router.push('/my-tasks')">
              查看全部
            </el-button>
          </div>
          <div class="card-body">
            <div v-if="loading.tasks" class="loading-container">
              <el-icon class="is-loading"><Loading /></el-icon>
              加载中...
            </div>
            <div v-else-if="myTasks.length === 0" class="empty-container">
              <el-icon class="empty-icon"><DocumentRemove /></el-icon>
              <div class="empty-text">暂无任务</div>
            </div>
            <div v-else class="task-list">
              <div 
                v-for="task in myTasks" 
                :key="task.id" 
                class="task-item"
                @click="$router.push(`/tasks/${task.id}`)"
              >
                <div class="task-info">
                  <div class="task-title">{{ task.title }}</div>
                  <div class="task-meta">
                    <el-tag 
                      :type="getTaskStatusInfo(task.status).type" 
                      size="small"
                    >
                      {{ getTaskStatusInfo(task.status).text }}
                    </el-tag>
                    <el-tag 
                      :type="getPriorityInfo(task.priority).type" 
                      size="small"
                    >
                      {{ getPriorityInfo(task.priority).text }}
                    </el-tag>
                    <span class="task-time">
                      {{ formatRelativeTime(task.due_date) }}
                    </span>
                  </div>
                </div>
                <div class="task-progress">
                  <el-progress 
                    :percentage="task.progress_percentage || 0" 
                    :stroke-width="6"
                    :show-text="false"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 最近通知 -->
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">最近通知</h3>
            <el-button text @click="$router.push('/notifications')">
              查看全部
            </el-button>
          </div>
          <div class="card-body">
            <div v-if="loading.notifications" class="loading-container">
              <el-icon class="is-loading"><Loading /></el-icon>
              加载中...
            </div>
            <div v-else-if="notifications.length === 0" class="empty-container">
              <el-icon class="empty-icon"><Bell /></el-icon>
              <div class="empty-text">暂无通知</div>
            </div>
            <div v-else class="notification-list">
              <div 
                v-for="notification in notifications" 
                :key="notification.id" 
                class="notification-item"
                :class="{ unread: notification.status === 'unread' }"
              >
                <div class="notification-content">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-time">
                    {{ formatRelativeTime(notification.created_at) }}
                  </div>
                </div>
                <div v-if="notification.status === 'unread'" class="unread-dot"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-right">
        <!-- 任务统计图表 -->
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">任务状态分布</h3>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <v-chart 
                v-if="chartData.length > 0"
                :option="chartOption" 
                style="height: 300px;"
              />
              <div v-else class="empty-container">
                <el-icon class="empty-icon"><PieChart /></el-icon>
                <div class="empty-text">暂无数据</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快捷操作 -->
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">快捷操作</h3>
          </div>
          <div class="card-body">
            <div class="quick-actions">
              <div 
                v-if="canCreateTask"
                class="quick-action-item" 
                @click="$router.push('/tasks/create')"
              >
                <el-icon><Plus /></el-icon>
                <span>创建任务</span>
              </div>
              <div class="quick-action-item" @click="$router.push('/my-tasks')">
                <el-icon><User /></el-icon>
                <span>我的任务</span>
              </div>
              <div class="quick-action-item" @click="$router.push('/tasks')">
                <el-icon><List /></el-icon>
                <span>任务列表</span>
              </div>
              <div class="quick-action-item" @click="$router.push('/reports')">
                <el-icon><DataAnalysis /></el-icon>
                <span>统计报表</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { VChart, defaultPieOptions, chartColors } from '@/plugins/echarts'
import { useUserStore } from '@/stores/user'
import { getTaskStatistics, getMyTasks } from '@/api/tasks'
import { formatDate, formatRelativeTime, getTaskStatusInfo, getPriorityInfo } from '@/utils'

const userStore = useUserStore()

// 响应式数据
const stats = ref({})
const myTasks = ref([])
const notifications = ref([])
const chartData = ref([])

const loading = reactive({
  tasks: false,
  notifications: false,
  stats: false
})

// 计算属性
const userInfo = computed(() => userStore.userInfo)
const canCreateTask = computed(() => userStore.canCreateTask)

const chartOption = computed(() => ({
  ...defaultPieOptions,
  series: [
    {
      name: '任务状态',
      type: 'pie',
      radius: '50%',
      data: chartData.value.map((item, index) => ({
        ...item,
        itemStyle: {
          color: chartColors[index % chartColors.length]
        }
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}))

// 方法
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 17) return '下午好'
  if (hour < 19) return '傍晚好'
  return '晚上好'
}

const fetchStats = async () => {
  try {
    loading.stats = true
    const response = await getTaskStatistics()
    stats.value = response.data
    
    // 构建图表数据
    const statusStats = response.data.status_stats || {}
    chartData.value = Object.keys(statusStats).map(key => ({
      name: statusStats[key].name,
      value: statusStats[key].count
    })).filter(item => item.value > 0)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    loading.stats = false
  }
}

const fetchMyTasks = async () => {
  try {
    loading.tasks = true
    const response = await getMyTasks({ page_size: 5 })
    myTasks.value = response.data.results || response.data || []
  } catch (error) {
    console.error('获取我的任务失败:', error)
  } finally {
    loading.tasks = false
  }
}

const fetchNotifications = async () => {
  try {
    loading.notifications = true
    // 这里应该调用获取通知的API
    // const response = await getNotifications({ page_size: 5 })
    // notifications.value = response.data.results || response.data || []
    
    // 临时模拟数据
    notifications.value = [
      {
        id: 1,
        title: '您有新的任务分配',
        status: 'unread',
        created_at: new Date()
      },
      {
        id: 2,
        title: '任务"设备检修"已完成',
        status: 'read',
        created_at: new Date(Date.now() - 3600000)
      }
    ]
  } catch (error) {
    console.error('获取通知失败:', error)
  } finally {
    loading.notifications = false
  }
}

// 生命周期
onMounted(() => {
  fetchStats()
  fetchMyTasks()
  fetchNotifications()
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 24px;
  background: var(--bg-color-page);
  min-height: calc(100vh - 50px);
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px;
  background: var(--bg-color);
  border-radius: 8px;
  box-shadow: var(--box-shadow-base);

  .welcome-content {
    .welcome-title {
      font-size: 28px;
      font-weight: 600;
      color: var(--text-color-primary);
      margin: 0 0 8px 0;
    }

    .welcome-subtitle {
      font-size: 16px;
      color: var(--text-color-secondary);
      margin: 0;
    }
  }
}

.stats-section {
  margin-bottom: 24px;

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
  }

  .stat-card {
    background: var(--bg-color);
    border-radius: 8px;
    padding: 24px;
    box-shadow: var(--box-shadow-base);
    display: flex;
    align-items: center;
    transition: transform 0.2s;

    &:hover {
      transform: translateY(-2px);
    }

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      font-size: 24px;

      &.pending {
        background: rgba(230, 162, 60, 0.1);
        color: #e6a23c;
      }

      &.completed {
        background: rgba(103, 194, 58, 0.1);
        color: #67c23a;
      }

      &.overdue {
        background: rgba(245, 108, 108, 0.1);
        color: #f56c6c;
      }

      &.total {
        background: rgba(64, 158, 255, 0.1);
        color: #409eff;
      }
    }

    .stat-content {
      .stat-number {
        font-size: 32px;
        font-weight: 600;
        color: var(--text-color-primary);
        line-height: 1;
        margin-bottom: 4px;
      }

      .stat-label {
        font-size: 14px;
        color: var(--text-color-secondary);
      }
    }
  }
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.card {
  background: var(--bg-color);
  border-radius: 8px;
  box-shadow: var(--box-shadow-base);
  margin-bottom: 24px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color-extra-light);

    .card-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-color-primary);
      margin: 0;
    }
  }

  .card-body {
    padding: 24px;
  }
}

.task-list {
  .task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid var(--border-color-extra-light);
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: var(--bg-color-page);
    }

    &:last-child {
      border-bottom: none;
    }

    .task-info {
      flex: 1;

      .task-title {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-color-primary);
        margin-bottom: 8px;
      }

      .task-meta {
        display: flex;
        align-items: center;
        gap: 8px;

        .task-time {
          font-size: 12px;
          color: var(--text-color-secondary);
        }
      }
    }

    .task-progress {
      width: 100px;
      margin-left: 16px;
    }
  }
}

.notification-list {
  .notification-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color-extra-light);

    &:last-child {
      border-bottom: none;
    }

    &.unread {
      background-color: rgba(64, 158, 255, 0.05);
    }

    .notification-content {
      flex: 1;

      .notification-title {
        font-size: 14px;
        color: var(--text-color-primary);
        margin-bottom: 4px;
      }

      .notification-time {
        font-size: 12px;
        color: var(--text-color-secondary);
      }
    }

    .unread-dot {
      width: 8px;
      height: 8px;
      background: #409eff;
      border-radius: 50%;
    }
  }
}

.chart-container {
  height: 300px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;

  .quick-action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border: 1px solid var(--border-color-lighter);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      border-color: var(--primary-color);
      background-color: rgba(64, 158, 255, 0.05);
    }

    .el-icon {
      font-size: 24px;
      color: var(--primary-color);
      margin-bottom: 8px;
    }

    span {
      font-size: 14px;
      color: var(--text-color-primary);
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }

  .welcome-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
