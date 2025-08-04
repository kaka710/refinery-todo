<template>
  <div class="department-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><OfficeBuilding /></el-icon>
            部门管理
          </h1>
          <p class="page-subtitle">管理组织架构和部门信息</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="handleCreate" size="large">
            <el-icon><Plus /></el-icon>
            新建部门
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧部门列表 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <el-card class="department-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>部门列表</span>
                <el-input
                  v-model="searchText"
                  placeholder="搜索部门名称"
                  style="width: 200px"
                  clearable
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </div>
            </template>

            <el-table 
              :data="filteredDepartments" 
              v-loading="loading" 
              style="width: 100%"
              @row-click="handleRowClick"
              class="department-table"
            >
              <el-table-column prop="name" label="部门名称" min-width="120">
                <template #default="{ row }">
                  <div class="department-name">
                    <el-icon class="dept-icon"><OfficeBuilding /></el-icon>
                    <span>{{ row.name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="code" label="部门编码" width="100" />
              <el-table-column prop="description" label="部门描述" min-width="150" show-overflow-tooltip />
              <el-table-column prop="manager_name" label="部门经理" width="100">
                <template #default="{ row }">
                  <el-tag v-if="row.manager_name" size="small" type="success">
                    {{ row.manager_name }}
                  </el-tag>
                  <span v-else class="text-muted">未设置</span>
                </template>
              </el-table-column>
              <el-table-column prop="member_count" label="人员数量" width="100" align="center">
                <template #default="{ row }">
                  <div
                    class="member-count"
                    :class="getMemberCountClass(row.member_count)"
                    @click.stop="handleViewUsers(row)"
                    :title="`查看${row.name}的人员列表`"
                  >
                    <el-icon class="member-icon"><User /></el-icon>
                    <span class="member-number">{{ row.member_count }}</span>
                    <span class="member-unit">人</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="240" fixed="right">
                <template #default="{ row }">
                  <div class="action-buttons">
                    <el-button size="small" @click.stop="handleViewUsers(row)" class="action-btn">
                      <el-icon><User /></el-icon>
                      人员
                    </el-button>
                    <el-button size="small" @click.stop="handleEdit(row)" class="action-btn">
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-button>
                    <el-button size="small" type="danger" @click.stop="handleDelete(row)" class="action-btn">
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <!-- 右侧信息面板 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <div class="info-panels">
            <!-- 部门统计 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>部门统计</span>
                </div>
              </template>
              
              <div class="stats-content">
                <div class="stat-item">
                  <div class="stat-value">{{ departments.length }}</div>
                  <div class="stat-label">总部门数</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ totalMembers }}</div>
                  <div class="stat-label">总人员数</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ averageMembers }}</div>
                  <div class="stat-label">平均人员数</div>
                </div>
              </div>
            </el-card>

            <!-- 快速操作 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><Operation /></el-icon>
                  <span>快速操作</span>
                </div>
              </template>
              
              <div class="quick-actions">
                <el-button @click="handleCreate" class="quick-action-btn">
                  <el-icon><Plus /></el-icon>
                  <span>新建部门</span>
                </el-button>
                <el-button @click="handleImport" class="quick-action-btn">
                  <el-icon><Upload /></el-icon>
                  <span>导入部门</span>
                </el-button>
                <el-button @click="handleExport" class="quick-action-btn">
                  <el-icon><Download /></el-icon>
                  <span>导出部门</span>
                </el-button>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  OfficeBuilding, Plus, Search, User, Edit, Delete, 
  DataAnalysis, Operation, Upload, Download 
} from '@element-plus/icons-vue'

const router = useRouter()

const loading = ref(false)
const departments = ref([])
const searchText = ref('')

// 模拟数据
const mockDepartments = [
  {
    id: 1,
    name: '生产部',
    code: 'PROD',
    description: '负责生产运营和生产管理',
    manager_name: '顾志华',
    member_count: 25
  },
  {
    id: 2,
    name: '技术部',
    code: 'TECH',
    description: '负责技术研发和技术支持',
    manager_name: '张三',
    member_count: 18
  },
  {
    id: 3,
    name: '质量部',
    code: 'QC',
    description: '负责质量管控和质量检验',
    manager_name: '李四',
    member_count: 12
  },
  {
    id: 4,
    name: '安全部',
    code: 'SAFE',
    description: '负责安全管理和安全监督',
    manager_name: '王五',
    member_count: 15
  },
  {
    id: 5,
    name: '设备部',
    code: 'EQUIP',
    description: '负责设备维护和设备管理',
    manager_name: '赵六',
    member_count: 20
  }
]

// 过滤后的部门列表
const filteredDepartments = computed(() => {
  if (!searchText.value) return departments.value
  return departments.value.filter(dept => 
    dept.name.toLowerCase().includes(searchText.value.toLowerCase()) ||
    dept.code.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

// 总人员数
const totalMembers = computed(() => {
  return departments.value.reduce((sum, dept) => sum + dept.member_count, 0)
})

// 平均人员数
const averageMembers = computed(() => {
  if (departments.value.length === 0) return 0
  return Math.round(totalMembers.value / departments.value.length)
})

// 加载部门列表
const loadDepartments = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    departments.value = mockDepartments
  } catch (error) {
    ElMessage.error('加载部门列表失败')
  } finally {
    loading.value = false
  }
}

// 处理行点击
const handleRowClick = (row) => {
  handleViewUsers(row)
}

// 获取人员数量样式类
const getMemberCountClass = (count) => {
  if (count >= 20) return 'member-count-large'
  if (count >= 10) return 'member-count-medium'
  if (count >= 5) return 'member-count-small'
  return 'member-count-mini'
}

// 查看部门人员
const handleViewUsers = (row) => {
  router.push({ name: 'DepartmentUsers', params: { id: row.id } })
}

// 创建部门
const handleCreate = () => {
  ElMessage.info('创建部门功能开发中...')
}

// 编辑部门
const handleEdit = (row) => {
  ElMessage.info(`编辑部门 ${row.name} 功能开发中...`)
}

// 删除部门
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除部门 "${row.name}" 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success(`部门 ${row.name} 删除成功`)
    // 这里应该调用删除API
    loadDepartments()
  } catch {
    // 用户取消删除
  }
}

// 导入部门
const handleImport = () => {
  ElMessage.info('导入部门功能开发中...')
}

// 导出部门
const handleExport = () => {
  ElMessage.info('导出部门功能开发中...')
}

onMounted(() => {
  loadDepartments()
})
</script>

<style scoped>
.department-list {
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 0;
}

/* 页面头部样式 */
.page-header {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  padding: 24px 32px;
  margin-bottom: 24px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-subtitle {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

/* 主要内容区域 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px 32px;
}

/* 卡片样式 */
.department-card, .info-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.info-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

/* 表格样式 */
.department-table {
  cursor: pointer;
}

.department-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dept-icon {
  color: #409eff;
}

.text-muted {
  color: #909399;
}

/* 人员数量样式 */
.member-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 70px;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.member-count::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.member-count:hover::before {
  left: 100%;
}

.member-count:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 不同人员数量范围的样式 */
.member-count-mini {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 1px solid #ff9800;
  color: #e65100;
}

.member-count-mini:hover {
  background: linear-gradient(135deg, #ffe0b2 0%, #ffcc02 100%);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
}

.member-count-small {
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
  border: 1px solid #4caf50;
  color: #2e7d32;
}

.member-count-small:hover {
  background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.member-count-medium {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border: 1px solid #2196f3;
  color: #1565c0;
}

.member-count-medium:hover {
  background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.member-count-large {
  background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
  border: 1px solid #e91e63;
  color: #ad1457;
}

.member-count-large:hover {
  background: linear-gradient(135deg, #f8bbd9 0%, #f48fb1 100%);
  box-shadow: 0 4px 12px rgba(233, 30, 99, 0.3);
}

.member-icon {
  font-size: 14px;
}

.member-number {
  font-weight: 600;
  font-size: 14px;
}

.member-unit {
  font-size: 12px;
  opacity: 0.8;
}

/* 统计样式 */
.stats-content {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 快速操作样式 */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-action-btn {
  width: 100%;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.quick-action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-action-btn .el-icon {
  font-size: 16px;
}

.quick-action-btn span {
  font-weight: 500;
}

/* 信息面板 */
.info-panels {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    padding: 16px 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .main-content {
    padding: 0 20px 20px;
  }
  
  .stats-content {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
