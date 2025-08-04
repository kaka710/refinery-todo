<template>
  <div class="my-tasks">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的任务</span>
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建任务
          </el-button>
        </div>
      </template>
      
      <!-- 统计卡片 -->
      <div class="stats-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ stats.total }}</div>
                <div class="stat-label">总任务</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number pending">{{ stats.pending }}</div>
                <div class="stat-label">待处理</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number in-progress">{{ stats.inProgress }}</div>
                <div class="stat-label">进行中</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number completed">{{ stats.completed }}</div>
                <div class="stat-label">已完成</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 任务列表 -->
      <div class="tasks-section">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="待处理" name="pending">
            <task-list :tasks="pendingTasks" @view="handleView" @edit="handleEdit" />
          </el-tab-pane>
          <el-tab-pane label="进行中" name="in_progress">
            <task-list :tasks="inProgressTasks" @view="handleView" @edit="handleEdit" />
          </el-tab-pane>
          <el-tab-pane label="已完成" name="completed">
            <task-list :tasks="completedTasks" @view="handleView" @edit="handleEdit" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()
const activeTab = ref('pending')
const loading = ref(false)
const tasks = ref([])

// 模拟数据
const mockTasks = [
  {
    id: 1,
    title: '完成项目需求分析',
    status: 'in_progress',
    priority: 'high',
    due_date: '2024-01-15'
  },
  {
    id: 2,
    title: '系统测试',
    status: 'pending',
    priority: 'medium',
    due_date: '2024-01-20'
  },
  {
    id: 3,
    title: '文档编写',
    status: 'completed',
    priority: 'low',
    due_date: '2024-01-10'
  }
]

// 计算属性
const stats = computed(() => {
  const total = tasks.value.length
  const pending = tasks.value.filter(t => t.status === 'pending').length
  const inProgress = tasks.value.filter(t => t.status === 'in_progress').length
  const completed = tasks.value.filter(t => t.status === 'completed').length
  
  return { total, pending, inProgress, completed }
})

const pendingTasks = computed(() => 
  tasks.value.filter(t => t.status === 'pending')
)

const inProgressTasks = computed(() => 
  tasks.value.filter(t => t.status === 'in_progress')
)

const completedTasks = computed(() => 
  tasks.value.filter(t => t.status === 'completed')
)

// 方法
const loadMyTasks = async () => {
  loading.value = true
  try {
    // 这里应该调用API获取我的任务
    // const response = await tasksApi.getMyTasks()
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    tasks.value = mockTasks
  } catch (error) {
    ElMessage.error('加载我的任务失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push('/tasks/create')
}

const handleView = (task) => {
  router.push(`/tasks/${task.id}`)
}

const handleEdit = (task) => {
  router.push(`/tasks/${task.id}/edit`)
}

const handleTabChange = (tabName) => {
  activeTab.value = tabName
}

onMounted(() => {
  loadMyTasks()
})
</script>

<script>
// 简单的任务列表组件
const TaskList = {
  props: ['tasks'],
  emits: ['view', 'edit'],
  template: `
    <div class="task-list">
      <div v-if="tasks.length === 0" class="empty-state">
        <el-empty description="暂无任务" />
      </div>
      <div v-else>
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-info">
            <h4>{{ task.title }}</h4>
            <div class="task-meta">
              <el-tag :type="getPriorityType(task.priority)" size="small">
                {{ getPriorityText(task.priority) }}
              </el-tag>
              <span class="due-date">截止: {{ task.due_date }}</span>
            </div>
          </div>
          <div class="task-actions">
            <el-button size="small" @click="$emit('view', task)">查看</el-button>
            <el-button size="small" type="primary" @click="$emit('edit', task)">编辑</el-button>
          </div>
        </div>
      </div>
    </div>
  `,
  methods: {
    getPriorityType(priority) {
      const types = {
        low: 'info',
        medium: '',
        high: 'warning',
        urgent: 'danger'
      }
      return types[priority] || ''
    },
    getPriorityText(priority) {
      const texts = {
        low: '低',
        medium: '中',
        high: '高',
        urgent: '紧急'
      }
      return texts[priority] || priority
    }
  }
}

export default {
  components: {
    TaskList
  }
}
</script>

<style scoped>
.my-tasks {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-number.pending {
  color: #909399;
}

.stat-number.in-progress {
  color: #e6a23c;
}

.stat-number.completed {
  color: #67c23a;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
}

.task-info h4 {
  margin: 0 0 8px 0;
  color: #303133;
}

.task-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.due-date {
  color: #909399;
  font-size: 12px;
}

.task-actions {
  display: flex;
  gap: 8px;
}
</style>
