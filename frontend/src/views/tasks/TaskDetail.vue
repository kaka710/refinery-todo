<template>
  <div class="task-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>任务详情</span>
          <div>
            <el-button @click="handleEdit">编辑</el-button>
            <el-button @click="handleBack">返回</el-button>
          </div>
        </div>
      </template>
      
      <div v-if="task" class="task-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务标题">
            {{ task.title }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(task.status)">
              {{ getStatusText(task.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="优先级">
            <el-tag :type="getPriorityType(task.priority)">
              {{ getPriorityText(task.priority) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="负责人">
            {{ task.assignee_name }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ task.created_at }}
          </el-descriptions-item>
          <el-descriptions-item label="截止日期">
            {{ task.due_date }}
          </el-descriptions-item>
          <el-descriptions-item label="任务描述" :span="2">
            {{ task.description }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const task = ref(null)

// 模拟任务数据
const mockTask = {
  id: 1,
  title: '完成项目需求分析',
  description: '分析项目需求，编写需求文档，确定技术方案',
  status: 'in_progress',
  priority: 'high',
  assignee_name: '张三',
  created_at: '2024-01-10 09:00:00',
  due_date: '2024-01-15'
}

const loadTask = async () => {
  loading.value = true
  try {
    const taskId = route.params.id
    
    // 这里应该调用API获取任务详情
    // const response = await tasksApi.getTask(taskId)
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    task.value = mockTask
  } catch (error) {
    ElMessage.error('加载任务详情失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = () => {
  router.push(`/tasks/${route.params.id}/edit`)
}

const handleBack = () => {
  router.back()
}

const getStatusType = (status) => {
  const types = {
    pending: '',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || ''
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const getPriorityType = (priority) => {
  const types = {
    low: 'info',
    medium: '',
    high: 'warning',
    urgent: 'danger'
  }
  return types[priority] || ''
}

const getPriorityText = (priority) => {
  const texts = {
    low: '低',
    medium: '中',
    high: '高',
    urgent: '紧急'
  }
  return texts[priority] || priority
}

onMounted(() => {
  loadTask()
})
</script>

<style scoped>
.task-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-info {
  margin-top: 20px;
}
</style>
