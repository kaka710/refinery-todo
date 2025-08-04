<template>
  <div class="task-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建任务
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchQuery"
              placeholder="搜索任务..."
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
              <el-option label="待处理" value="pending" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="priorityFilter" placeholder="优先级筛选" clearable>
              <el-option label="低" value="low" />
              <el-option label="中" value="medium" />
              <el-option label="高" value="high" />
              <el-option label="紧急" value="urgent" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 任务表格 -->
      <el-table :data="tasks" v-loading="loading" style="width: 100%">
        <el-table-column prop="title" label="任务标题" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">
              {{ getPriorityText(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignee_name" label="负责人" width="120" />
        <el-table-column prop="due_date" label="截止日期" width="120" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" @click="handleView(row)" class="action-btn">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="handleEdit(row)" class="action-btn">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)" class="action-btn">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, View, Edit, Delete } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const tasks = ref([])
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 模拟数据
const mockTasks = [
  {
    id: 1,
    title: '完成项目需求分析',
    status: 'in_progress',
    priority: 'high',
    assignee_name: '张三',
    due_date: '2024-01-15'
  },
  {
    id: 2,
    title: '系统测试',
    status: 'pending',
    priority: 'medium',
    assignee_name: '李四',
    due_date: '2024-01-20'
  }
]

// 方法
const loadTasks = async () => {
  loading.value = true
  try {
    // 这里应该调用API获取任务列表
    // const response = await tasksApi.getTasks(...)
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    tasks.value = mockTasks
    total.value = mockTasks.length
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push('/tasks/create')
}

const handleView = (row) => {
  router.push(`/tasks/${row.id}`)
}

const handleEdit = (row) => {
  router.push(`/tasks/${row.id}/edit`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '确认删除', {
      type: 'warning'
    })
    
    // 这里应该调用API删除任务
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error) {
    // 用户取消删除
  }
}

const handleSearch = () => {
  loadTasks()
}

const handleSizeChange = () => {
  loadTasks()
}

const handleCurrentChange = () => {
  loadTasks()
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

// 生命周期
onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.task-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
  align-items: center;
}

.action-btn {
  flex-shrink: 0;
  min-width: auto;
  padding: 4px 8px;
}
</style>
