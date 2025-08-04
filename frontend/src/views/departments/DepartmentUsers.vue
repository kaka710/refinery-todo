<template>
  <div class="department-users">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <el-button @click="handleBack" size="large" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
          <div class="title-section">
            <h1 class="page-title">
              <el-icon><OfficeBuilding /></el-icon>
              {{ departmentInfo.name }}
            </h1>
            <p class="page-subtitle">{{ departmentInfo.description }}</p>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="handleAddUser" size="large">
            <el-icon><Plus /></el-icon>
            添加人员
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧人员列表 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <el-card class="users-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>部门人员 ({{ filteredUsers.length }})</span>
                <div class="header-actions">
                  <el-input
                    v-model="searchText"
                    placeholder="搜索人员姓名或工号"
                    style="width: 200px; margin-right: 12px"
                    clearable
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>
                  </el-input>
                  <el-select v-model="roleFilter" placeholder="筛选角色" style="width: 120px" clearable>
                    <el-option label="全部" value="" />
                    <el-option label="部门经理" value="manager" />
                    <el-option label="执行人员" value="executor" />
                    <el-option label="协办人员" value="collaborator" />
                  </el-select>
                </div>
              </div>
            </template>

            <el-table 
              :data="filteredUsers" 
              v-loading="loading" 
              style="width: 100%"
              class="users-table"
            >
              <el-table-column prop="employee_id" label="工号" width="100" />
              <el-table-column prop="real_name" label="姓名" width="100">
                <template #default="{ row }">
                  <div class="user-name">
                    <el-avatar :size="32" :src="row.avatar">
                      <el-icon><User /></el-icon>
                    </el-avatar>
                    <span>{{ row.real_name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="position" label="职位" width="120" />
              <el-table-column prop="role" label="角色" width="100">
                <template #default="{ row }">
                  <el-tag :type="getRoleType(row.role)" size="small">
                    {{ getRoleText(row.role) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="phone" label="联系电话" width="130" />
              <el-table-column prop="email" label="邮箱" min-width="150" show-overflow-tooltip />
              <el-table-column prop="status" label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
                    {{ row.status === 'active' ? '在职' : '离职' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="220" fixed="right">
                <template #default="{ row }">
                  <div class="action-buttons">
                    <el-button size="small" @click="handleViewUser(row)" class="action-btn">
                      <el-icon><View /></el-icon>
                      详情
                    </el-button>
                    <el-button size="small" @click="handleEditUser(row)" class="action-btn">
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-button>
                    <el-button size="small" type="danger" @click="handleRemoveUser(row)" class="action-btn">
                      <el-icon><Remove /></el-icon>
                      移除
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
            <!-- 部门信息 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><InfoFilled /></el-icon>
                  <span>部门信息</span>
                </div>
              </template>
              
              <div class="dept-info">
                <div class="info-item">
                  <label>部门名称：</label>
                  <span>{{ departmentInfo.name }}</span>
                </div>
                <div class="info-item">
                  <label>部门编码：</label>
                  <span>{{ departmentInfo.code }}</span>
                </div>
                <div class="info-item">
                  <label>部门经理：</label>
                  <span>{{ departmentInfo.manager_name || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>人员数量：</label>
                  <span>{{ users.length }} 人</span>
                </div>
                <div class="info-item">
                  <label>部门描述：</label>
                  <span>{{ departmentInfo.description }}</span>
                </div>
              </div>
            </el-card>

            <!-- 人员统计 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>人员统计</span>
                </div>
              </template>
              
              <div class="stats-content">
                <div class="stat-item stat-total">
                  <div class="stat-icon">
                    <el-icon><User /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ users.length }}</div>
                    <div class="stat-label">总人数</div>
                  </div>
                </div>
                <div class="stat-item stat-active">
                  <div class="stat-icon">
                    <el-icon><UserFilled /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ activeUsers }}</div>
                    <div class="stat-label">在职人数</div>
                  </div>
                </div>
                <div class="stat-item stat-manager">
                  <div class="stat-icon">
                    <el-icon><Avatar /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ managerCount }}</div>
                    <div class="stat-label">管理人员</div>
                  </div>
                </div>
                <div class="stat-item stat-filtered">
                  <div class="stat-icon">
                    <el-icon><Search /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ filteredUsers.length }}</div>
                    <div class="stat-label">当前显示</div>
                  </div>
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
                <el-button @click="handleAddUser" class="quick-action-btn">
                  <el-icon><Plus /></el-icon>
                  <span>添加人员</span>
                </el-button>
                <el-button @click="handleImportUsers" class="quick-action-btn">
                  <el-icon><Upload /></el-icon>
                  <span>批量导入</span>
                </el-button>
                <el-button @click="handleExportUsers" class="quick-action-btn">
                  <el-icon><Download /></el-icon>
                  <span>导出名单</span>
                </el-button>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 用户详情对话框 -->
    <UserDetailDialog
      v-model="showUserDetailDialog"
      :user-id="selectedUserId"
      @edit="handleEditFromDetail"
    />

    <!-- 用户编辑对话框 -->
    <UserEditDialog
      v-model="showUserEditDialog"
      :mode="editMode"
      :user-id="editUserId"
      :departments="allDepartments"
      @success="handleEditSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft, OfficeBuilding, Plus, Search, User, View, Edit, Remove,
  InfoFilled, DataAnalysis, Operation, Upload, Download, UserFilled, Avatar
} from '@element-plus/icons-vue'
import UserDetailDialog from '@/components/UserDetailDialog.vue'
import UserEditDialog from '@/components/UserEditDialog.vue'
import { updateUser, getUserDetail } from '@/api/auth'
import { departmentsApi } from '@/api/departments'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const users = ref([])
const departmentInfo = ref({})
const searchText = ref('')
const roleFilter = ref('')
const showUserDetailDialog = ref(false)
const selectedUserId = ref(null)
const showUserEditDialog = ref(false)
const editMode = ref('create')
const editUserId = ref(null)
const allDepartments = ref([])

// 模拟部门信息 - 与数据库实际部门对应
const mockDepartmentInfo = {
  1: { id: 1, name: '技术部', code: 'TECH', description: '负责技术研发和技术支持', manager_name: '张三' },
  2: { id: 2, name: '生产部', code: 'PROD', description: '负责生产运营和生产管理', manager_name: '李四' },
  3: { id: 3, name: '质量部', code: 'QA', description: '负责质量管控和质量检验', manager_name: '王五' }
}

// 模拟用户数据 - 与数据库实际用户对应
const mockUsersByDepartment = {
  1: [ // 技术部
    { id: 2, employee_id: 'T001', real_name: '张三', position: '技术经理', role: 'prof_manager', phone: '13800138001', email: 'zhangsan@hnlh.com', status: 'active' },
    { id: 5, employee_id: 'T002', real_name: '赵六', position: '工程师', role: 'executor', phone: '13800138004', email: 'zhaoliu@hnlh.com', status: 'active' }
  ],
  2: [ // 生产部
    { id: 3, employee_id: 'P001', real_name: '李四', position: '部门经理', role: 'dept_manager', phone: '13800138002', email: 'lisi@hnlh.com', status: 'active' }
  ],
  3: [ // 质量部
    { id: 4, employee_id: 'Q001', real_name: '王五', position: '质量检验员', role: 'executor', phone: '13800138003', email: 'wangwu@hnlh.com', status: 'active' }
  ]
}

// 过滤后的用户列表
const filteredUsers = computed(() => {
  let result = users.value
  
  // 搜索过滤
  if (searchText.value) {
    result = result.filter(user => 
      user.real_name.toLowerCase().includes(searchText.value.toLowerCase()) ||
      user.employee_id.toLowerCase().includes(searchText.value.toLowerCase())
    )
  }
  
  // 角色过滤
  if (roleFilter.value) {
    result = result.filter(user => user.role === roleFilter.value)
  }
  
  return result
})

// 在职人数
const activeUsers = computed(() => {
  return users.value.filter(user => user.status === 'active').length
})

// 管理人员数量
const managerCount = computed(() => {
  return users.value.filter(user => user.role === 'manager').length
})

// 获取角色类型
const getRoleType = (role) => {
  const types = {
    manager: 'danger',
    executor: 'primary',
    collaborator: 'warning'
  }
  return types[role] || 'info'
}

// 获取角色文本
const getRoleText = (role) => {
  const texts = {
    manager: '部门经理',
    executor: '执行人员',
    collaborator: '协办人员'
  }
  return texts[role] || '未知'
}

// 加载部门信息和用户列表
const loadData = async () => {
  loading.value = true
  try {
    const departmentId = parseInt(route.params.id)

    // 加载所有部门数据（用于编辑对话框）
    try {
      const deptResponse = await departmentsApi.getDepartments()
      allDepartments.value = deptResponse.data || []
    } catch (error) {
      console.warn('加载部门数据失败，使用模拟数据:', error)
      allDepartments.value = Object.values(mockDepartmentInfo)
    }

    // 加载部门信息
    departmentInfo.value = mockDepartmentInfo[departmentId] || {}

    // 加载用户列表
    await new Promise(resolve => setTimeout(resolve, 500))
    users.value = mockUsersByDepartment[departmentId] || []
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 返回部门列表
const handleBack = () => {
  router.push({ name: 'DepartmentList' })
}

// 添加人员
const handleAddUser = () => {
  ElMessage.info('添加人员功能开发中...')
}

// 查看用户详情
const handleViewUser = (user) => {
  selectedUserId.value = user.id
  showUserDetailDialog.value = true
}

// 编辑用户
const handleEditUser = (user) => {
  editMode.value = 'edit'
  editUserId.value = user.id
  showUserEditDialog.value = true
}

// 从详情对话框编辑用户
const handleEditFromDetail = (user) => {
  handleEditUser(user)
}

// 编辑成功回调
const handleEditSuccess = () => {
  loadData() // 重新加载数据
}

// 移除用户
const handleRemoveUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要将 "${user.real_name}" 从部门中移除吗？`,
      '移除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success(`用户 ${user.real_name} 移除成功`)
    // 这里应该调用移除API
    loadData()
  } catch {
    // 用户取消移除
  }
}

// 批量导入用户
const handleImportUsers = () => {
  ElMessage.info('批量导入用户功能开发中...')
}

// 导出用户名单
const handleExportUsers = () => {
  ElMessage.info('导出用户名单功能开发中...')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.department-users {
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 0;
}

/* 页面头部样式 */
.page-header {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  padding: 32px 40px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 32px;
  flex: 1;
}

.back-btn {
  flex-shrink: 0;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateX(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.title-section {
  flex: 1;
  max-width: 600px;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 12px;
  line-height: 1.2;
}

.page-title .el-icon {
  font-size: 32px;
  color: #409eff;
}

.page-subtitle {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 15px;
  line-height: 1.4;
}

.header-right {
  flex-shrink: 0;
  margin-left: 24px;
}

.header-right .el-button {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 15px;
  transition: all 0.3s ease;
}

.header-right .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.3);
}

/* 主要内容区域 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px 32px;
}

/* 卡片样式 */
.users-card, .info-card {
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

.header-actions {
  display: flex;
  align-items: center;
}

.info-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

/* 用户表格样式 */
.user-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 部门信息样式 */
.dept-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item label {
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.info-item span {
  font-size: 14px;
  color: #303133;
}

/* 统计样式 */
.stats-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
  min-width: 0; /* 防止内容溢出 */
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.stat-info {
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
  overflow: hidden;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 12px;
  opacity: 0.8;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 不同统计项的主题色 */
.stat-total {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border: 1px solid #2196f3;
}

.stat-total .stat-icon {
  background: #2196f3;
  color: white;
}

.stat-total .stat-value {
  color: #1565c0;
}

.stat-total .stat-label {
  color: #1976d2;
}

.stat-active {
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
  border: 1px solid #4caf50;
}

.stat-active .stat-icon {
  background: #4caf50;
  color: white;
}

.stat-active .stat-value {
  color: #2e7d32;
}

.stat-active .stat-label {
  color: #388e3c;
}

.stat-manager {
  background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
  border: 1px solid #e91e63;
}

.stat-manager .stat-icon {
  background: #e91e63;
  color: white;
}

.stat-manager .stat-value {
  color: #ad1457;
}

.stat-manager .stat-label {
  color: #c2185b;
}

.stat-filtered {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 1px solid #ff9800;
}

.stat-filtered .stat-icon {
  background: #ff9800;
  color: white;
}

.stat-filtered .stat-value {
  color: #e65100;
}

.stat-filtered .stat-label {
  color: #f57c00;
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
    padding: 20px 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
    min-height: auto;
  }

  .header-left {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .title-section {
    max-width: none;
  }

  .page-title {
    font-size: 24px;
  }

  .page-title .el-icon {
    font-size: 28px;
  }

  .header-right {
    width: 100%;
    margin-left: 0;
  }

  .header-right .el-button {
    width: 100%;
    justify-content: center;
  }
  
  .main-content {
    padding: 0 20px 20px;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }
  
  .stats-content {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
  }

  .stat-item {
    padding: 12px;
  }

  .stat-value {
    font-size: 20px;
  }

  .stat-label {
    font-size: 11px;
  }
}
</style>
