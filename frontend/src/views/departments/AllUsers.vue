<template>
  <div class="all-users">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><UserFilled /></el-icon>
            全部人员
          </h1>
          <p class="page-subtitle">管理所有部门的人员信息</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="handleCreate" size="large">
            <el-icon><Plus /></el-icon>
            新建用户
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧用户列表 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <el-card class="users-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>用户列表 ({{ filteredUsers.length }})</span>
                <div class="header-actions">
                  <el-input
                    v-model="searchText"
                    placeholder="搜索姓名、工号或邮箱"
                    style="width: 200px; margin-right: 12px"
                    clearable
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>
                  </el-input>
                  <el-select v-model="departmentFilter" placeholder="筛选部门" style="width: 120px; margin-right: 12px" clearable>
                    <el-option label="全部部门" value="" />
                    <el-option
                      v-for="dept in departments"
                      :key="dept.id || dept.name"
                      :label="dept.name || '未知部门'"
                      :value="dept.id || ''"
                      v-if="dept && dept.id !== null && dept.id !== undefined"
                    />
                  </el-select>
                  <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 100px" clearable>
                    <el-option label="全部" value="" />
                    <el-option label="在职" value="active" />
                    <el-option label="离职" value="inactive" />
                  </el-select>
                </div>
              </div>
            </template>

            <el-table
              :data="paginatedUsers"
              v-loading="loading"
              style="width: 100%"
              class="users-table"
              row-key="id"
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
              <el-table-column prop="department_name" label="部门" width="100">
                <template #default="{ row }">
                  <el-tag size="small" type="primary">{{ row.department_name }}</el-tag>
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
                    <el-button size="small" @click="handleView(row)" class="action-btn">
                      <el-icon><View /></el-icon>
                      详情
                    </el-button>
                    <el-button size="small" @click="handleEdit(row)" class="action-btn">
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
            <div class="pagination-wrapper">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="filteredUsers.length"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 右侧信息面板 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <div class="info-panels">
            <!-- 用户统计 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>人员统计</span>
                </div>
              </template>

              <div class="stats-grid">
                <div class="stat-card total">
                  <div class="stat-icon">
                    <el-icon><UserFilled /></el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ allUsers.length }}</div>
                    <div class="stat-label">总人数</div>
                  </div>
                </div>

                <div class="stat-card active">
                  <div class="stat-icon">
                    <el-icon><User /></el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ activeUsers }}</div>
                    <div class="stat-label">在职人员</div>
                  </div>
                </div>

                <div class="stat-card manager">
                  <div class="stat-icon">
                    <el-icon><Operation /></el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ managerCount }}</div>
                    <div class="stat-label">管理人员</div>
                  </div>
                </div>

                <div class="stat-card executor">
                  <div class="stat-icon">
                    <el-icon><User /></el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ roleStats.executor }}</div>
                    <div class="stat-label">执行人员</div>
                  </div>
                </div>
              </div>

              <!-- 角色详细统计 -->
              <div class="role-details">
                <div class="role-item">
                  <span class="role-name">系统管理员</span>
                  <span class="role-count">{{ roleStats.admin }}</span>
                </div>
                <div class="role-item">
                  <span class="role-name">部门负责人</span>
                  <span class="role-count">{{ roleStats.dept_manager }}</span>
                </div>
                <div class="role-item">
                  <span class="role-name">专业负责人</span>
                  <span class="role-count">{{ roleStats.prof_manager }}</span>
                </div>
                <div class="role-item">
                  <span class="role-name">执行人员</span>
                  <span class="role-count">{{ roleStats.executor }}</span>
                </div>
              </div>
            </el-card>

            <!-- 部门分布 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><PieChart /></el-icon>
                  <span>部门分布</span>
                </div>
              </template>
              
              <div class="dept-distribution">
                <div 
                  v-for="dept in departmentStats" 
                  :key="dept.id" 
                  class="dept-stat-item"
                >
                  <div class="dept-info">
                    <span class="dept-name">{{ dept.name }}</span>
                    <span class="dept-count">{{ dept.count }} 人</span>
                  </div>
                  <el-progress 
                    :percentage="dept.percentage" 
                    :stroke-width="8"
                    :show-text="false"
                  />
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
                  <span>新建用户</span>
                </el-button>
                <el-button @click="handleImport" class="quick-action-btn">
                  <el-icon><Upload /></el-icon>
                  <span>批量导入</span>
                </el-button>
                <el-button @click="handleExport" class="quick-action-btn">
                  <el-icon><Download /></el-icon>
                  <span>导出用户</span>
                </el-button>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="showUserDialog"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
        class="user-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="userForm.username"
                placeholder="请输入用户名"
                :disabled="dialogMode === 'edit'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="userForm.real_name" placeholder="请输入真实姓名" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工号" prop="employee_id">
              <el-input v-model="userForm.employee_id" placeholder="请输入工号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门" prop="department_id">
              <el-select v-model="userForm.department_id" placeholder="请选择部门" style="width: 100%">
                <el-option
                  v-for="dept in departments"
                  :key="dept.id || dept.name"
                  :label="dept.name || '未知部门'"
                  :value="dept.id || ''"
                  v-if="dept && dept.id !== null && dept.id !== undefined"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userForm.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="userForm.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department_id">
              <el-select v-model="userForm.department_id" placeholder="请选择部门">
                <el-option
                  v-for="dept in departments"
                  :key="dept.id || dept.name"
                  :label="dept.name || '未知部门'"
                  :value="dept.id || ''"
                  v-if="dept && dept.id !== null && dept.id !== undefined"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="userForm.role" placeholder="请选择角色">
                <el-option label="系统管理员" value="admin" />
                <el-option label="部门负责人" value="dept_manager" />
                <el-option label="专业负责人" value="prof_manager" />
                <el-option label="执行人员" value="executor" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="职位" prop="position">
          <el-input v-model="userForm.position" placeholder="请输入职位" />
        </el-form-item>

        <el-form-item label="状态">
          <el-switch
            v-model="userForm.is_active"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>

        <template v-if="dialogMode === 'create'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="密码" prop="password">
                <el-input
                  v-model="userForm.password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="确认密码" prop="confirm_password">
                <el-input
                  v-model="userForm.confirm_password"
                  type="password"
                  placeholder="请再次输入密码"
                  show-password
                />
              </el-form-item>
            </el-col>
          </el-row>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="showUserDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveUser" :loading="saving">
          {{ dialogMode === 'create' ? '创建' : '保存' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 导入用户对话框 -->
    <el-dialog
      v-model="showImportDialog"
      title="批量导入用户"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="import-content">
        <div class="import-tips">
          <h4>导入说明：</h4>
          <ul>
            <li>支持 Excel (.xlsx) 和 CSV (.csv) 格式</li>
            <li>第一行必须为表头：工号、姓名、用户名、邮箱、手机号、部门、职位</li>
            <li>工号和姓名为必填项</li>
            <li>邮箱格式必须正确</li>
            <li>部门名称必须与系统中的部门名称完全一致</li>
          </ul>
        </div>

        <div class="import-actions">
          <el-button @click="downloadTemplate">
            <el-icon><Download /></el-icon>
            下载模板
          </el-button>
        </div>

        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :show-file-list="true"
          :limit="1"
          accept=".xlsx,.csv"
          @change="handleFileChange"
          class="import-upload"
        >
          <el-button type="primary">
            <el-icon><Upload /></el-icon>
            选择文件
          </el-button>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 xlsx/csv 文件，且不超过 10MB
            </div>
          </template>
        </el-upload>

        <div v-if="importProgress > 0" class="import-progress">
          <el-progress :percentage="importProgress" :status="importProgress === 100 ? 'success' : 'active'" />
        </div>

        <div v-if="importResult" class="import-result">
          <el-alert
            :title="`导入完成：成功 ${importResult.success} 条，失败 ${importResult.failed} 条`"
            :type="importResult.failed > 0 ? 'warning' : 'success'"
            show-icon
            :closable="false"
          />
          <div v-if="importResult.errors && importResult.errors.length > 0" class="import-errors">
            <h5>错误详情：</h5>
            <ul>
              <li v-for="(error, index) in importResult.errors" :key="index">
                第 {{ error.row }} 行：{{ error.message }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleImportUsers"
          :loading="importing"
          :disabled="!importFile"
        >
          开始导入
        </el-button>
      </template>
    </el-dialog>

    <!-- 用户详情对话框 -->
    <UserDetailDialog
      v-model="showUserDetailDialog"
      :user-id="selectedUserId"
      @edit="handleEditFromDetail"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  UserFilled, Plus, Search, User, View, Edit, Delete,
  DataAnalysis, PieChart, Operation, Upload, Download
} from '@element-plus/icons-vue'
import UserDetailDialog from '@/components/UserDetailDialog.vue'
import { updateUser, createUser, getUserDetail } from '@/api/auth'
import { departmentsApi } from '@/api/departments'

const loading = ref(false)
const allUsers = ref([])
const departments = ref([])
const searchText = ref('')
const departmentFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)

// 对话框相关
const showUserDialog = ref(false)
const showImportDialog = ref(false)
const showUserDetailDialog = ref(false)
const selectedUserId = ref(null)
const dialogMode = ref('create') // 'create' | 'edit'
const dialogTitle = ref('新建用户')
const saving = ref(false)
const importing = ref(false)

// 用户表单
const userForm = reactive({
  id: null,
  username: '',
  real_name: '',
  email: '',
  phone: '',
  employee_id: '',
  department_id: '',
  role: 'executor',
  position: '',
  is_active: true,
  password: '',
  confirm_password: ''
})

// 导入相关
const importFile = ref(null)
const importProgress = ref(0)
const importResult = ref(null)
const userFormRef = ref()
const uploadRef = ref()

// 表单验证规则
const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  employee_id: [
    { required: true, message: '请输入工号', trigger: 'blur' }
  ],
  department_id: [
    { required: true, message: '请选择部门', trigger: 'change' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== userForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 模拟部门数据 - 与数据库实际部门对应
const mockDepartments = [
  { id: 1, name: '技术部', code: 'TECH' },
  { id: 2, name: '生产部', code: 'PROD' },
  { id: 3, name: '质量部', code: 'QA' }
]

// 模拟用户数据 - 与数据库实际用户对应
const mockAllUsers = [
  // 管理员
  { id: 1, employee_id: 'ADMIN', real_name: '系统管理员', department_id: 1, department_name: '技术部', position: '系统管理员', role: 'admin', phone: '13800138000', email: 'admin@hnlh.com', status: 'active' },
  // 技术部
  { id: 2, employee_id: 'T001', real_name: '张三', department_id: 1, department_name: '技术部', position: '技术经理', role: 'prof_manager', phone: '13800138001', email: 'zhangsan@hnlh.com', status: 'active' },
  { id: 5, employee_id: 'T002', real_name: '赵六', department_id: 1, department_name: '技术部', position: '工程师', role: 'executor', phone: '13800138004', email: 'zhaoliu@hnlh.com', status: 'active' },
  // 生产部
  { id: 3, employee_id: 'P001', real_name: '李四', department_id: 2, department_name: '生产部', position: '部门经理', role: 'dept_manager', phone: '13800138002', email: 'lisi@hnlh.com', status: 'active' },
  // 质量部
  { id: 4, employee_id: 'Q001', real_name: '王五', department_id: 3, department_name: '质量部', position: '质量检验员', role: 'executor', phone: '13800138003', email: 'wangwu@hnlh.com', status: 'active' }
]

// 过滤后的用户列表
const filteredUsers = computed(() => {
  let result = allUsers.value

  // 搜索过滤
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(user =>
      user.real_name.toLowerCase().includes(search) ||
      user.employee_id.toLowerCase().includes(search) ||
      user.email.toLowerCase().includes(search)
    )
  }

  // 部门过滤
  if (departmentFilter.value) {
    result = result.filter(user => user.department_id === departmentFilter.value)
  }

  // 状态过滤
  if (statusFilter.value) {
    result = result.filter(user => user.status === statusFilter.value)
  }

  return result
})

// 分页后的用户列表
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredUsers.value.slice(start, end)
})

// 在职用户数
const activeUsers = computed(() => {
  return allUsers.value.filter(user => user.status === 'active').length
})

// 管理人员数量（包括系统管理员、部门负责人、专业负责人）
const managerCount = computed(() => {
  return allUsers.value.filter(user =>
    ['admin', 'dept_manager', 'prof_manager'].includes(user.role)
  ).length
})

// 各角色统计
const roleStats = computed(() => {
  const stats = {
    admin: 0,
    dept_manager: 0,
    prof_manager: 0,
    executor: 0
  }

  allUsers.value.forEach(user => {
    if (stats.hasOwnProperty(user.role)) {
      stats[user.role]++
    }
  })

  return stats
})

// 部门统计
const departmentStats = computed(() => {
  const stats = departments.value.map(dept => {
    const count = allUsers.value.filter(user => user.department_id === dept.id).length
    const percentage = allUsers.value.length > 0 ? Math.round((count / allUsers.value.length) * 100) : 0
    return {
      id: dept.id,
      name: dept.name,
      count,
      percentage
    }
  })
  return stats.sort((a, b) => b.count - a.count)
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

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载部门数据
    try {
      const deptResponse = await departmentsApi.getDepartments()
      departments.value = deptResponse.data || mockDepartments
    } catch (error) {
      console.warn('加载部门数据失败，使用模拟数据:', error)
      departments.value = mockDepartments
    }

    // 使用模拟用户数据（实际项目中应该调用用户列表API）
    allUsers.value = mockAllUsers
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 处理分页大小变更
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

// 处理当前页变更
const handleCurrentChange = (page) => {
  currentPage.value = page
}

// 创建用户
const handleCreate = () => {
  showUserDialog.value = true
  dialogMode.value = 'create'
  dialogTitle.value = '新建用户'

  // 重置表单
  Object.assign(userForm, {
    id: null,
    username: '',
    real_name: '',
    email: '',
    phone: '',
    employee_id: '',
    department_id: '',
    role: 'executor',
    position: '',
    is_active: true,
    password: '',
    confirm_password: ''
  })
}

// 查看用户详情
const handleView = (user) => {
  selectedUserId.value = user.id
  showUserDetailDialog.value = true
}

// 编辑用户
const handleEdit = async (user) => {
  try {
    // 获取用户详细信息
    const response = await getUserDetail(user.id)
    const userDetail = response.data

    showUserDialog.value = true
    dialogMode.value = 'edit'
    dialogTitle.value = '编辑用户'

    // 填充表单数据
    Object.assign(userForm, {
      id: userDetail.id,
      username: userDetail.username,
      real_name: userDetail.real_name,
      email: userDetail.email,
      phone: userDetail.phone,
      employee_id: userDetail.employee_id,
      department_id: userDetail.department?.id || '',
      role: userDetail.role || 'executor',
      position: userDetail.profile?.position || '',
      is_active: userDetail.is_active,
      password: '',
      confirm_password: ''
    })
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败')
  }
}

// 从详情对话框编辑用户
const handleEditFromDetail = (user) => {
  handleEdit(user)
}

// 删除用户
const handleDelete = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.real_name}" 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success(`用户 ${user.real_name} 删除成功`)
    // 这里应该调用删除API
    loadData()
  } catch {
    // 用户取消删除
  }
}

// 导入用户
const handleImport = () => {
  showImportDialog.value = true
}

// 导出用户
const handleExport = async () => {
  try {
    ElMessage.info('正在生成用户数据，请稍候...')

    // 模拟导出
    await new Promise(resolve => setTimeout(resolve, 2000))

    // 创建CSV数据
    const csvData = [
      ['工号', '姓名', '用户名', '邮箱', '手机号', '部门', '职位', '状态'],
      ...filteredUsers.value.map(user => [
        user.employee_id,
        user.real_name,
        user.username,
        user.email,
        user.phone,
        user.department_name,
        user.position,
        user.is_active ? '启用' : '禁用'
      ])
    ]

    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })

    // 创建下载链接
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `用户数据_${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    ElMessage.success('用户数据导出成功')
  } catch (error) {
    console.error('导出用户数据失败:', error)
    ElMessage.error('导出用户数据失败')
  }
}

// 保存用户
const handleSaveUser = async () => {
  try {
    await userFormRef.value.validate()

    saving.value = true

    // 准备提交数据
    const submitData = {
      username: userForm.username,
      real_name: userForm.real_name,
      email: userForm.email,
      phone: userForm.phone,
      employee_id: userForm.employee_id,
      department: userForm.department_id,
      role: userForm.role,
      is_active: userForm.is_active
    }

    // 如果有密码，添加密码字段
    if (userForm.password) {
      submitData.password = userForm.password
    }

    if (dialogMode.value === 'create') {
      // 创建新用户
      const response = await createUser(submitData)
      const newUser = response.data

      // 添加到本地列表
      allUsers.value.unshift({
        id: newUser.id,
        username: newUser.username,
        real_name: newUser.real_name,
        email: newUser.email,
        phone: newUser.phone,
        employee_id: newUser.employee_id,
        department_id: newUser.department?.id,
        department_name: newUser.department?.name || '',
        position: userForm.position,
        role: newUser.role,
        is_active: newUser.is_active,
        status: newUser.status
      })

      ElMessage.success('用户创建成功')
    } else {
      // 更新用户
      const response = await updateUser(userForm.id, submitData)
      const updatedUser = response.data

      // 更新本地列表
      const index = allUsers.value.findIndex(u => u.id === userForm.id)
      if (index > -1) {
        Object.assign(allUsers.value[index], {
          real_name: updatedUser.real_name,
          email: updatedUser.email,
          phone: updatedUser.phone,
          employee_id: updatedUser.employee_id,
          department_id: updatedUser.department?.id,
          department_name: updatedUser.department?.name || '',
          position: userForm.position,
          is_active: updatedUser.is_active
        })
      }

      ElMessage.success('用户信息更新成功')
    }

    showUserDialog.value = false
  } catch (error) {
    if (error !== false) { // 不是表单验证错误
      console.error('保存用户失败:', error)
      const errorMsg = error.response?.data?.message || error.message || '保存用户失败'
      ElMessage.error(errorMsg)
    }
  } finally {
    saving.value = false
  }
}

// 下载导入模板
const downloadTemplate = () => {
  const templateData = [
    ['工号', '姓名', '用户名', '邮箱', '手机号', '部门', '职位'],
    ['EMP001', '张三', 'zhangsan', 'zhangsan@example.com', '13800138001', '技术部', '高级工程师'],
    ['EMP002', '李四', 'lisi', 'lisi@example.com', '13800138002', '生产部', '操作员']
  ]

  const csvContent = templateData.map(row => row.join(',')).join('\n')
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })

  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = '用户导入模板.csv'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  ElMessage.success('模板下载成功')
}

// 处理文件选择
const handleFileChange = (file) => {
  importFile.value = file.raw
  importProgress.value = 0
  importResult.value = null
}

// 导入用户
const handleImportUsers = async () => {
  if (!importFile.value) {
    ElMessage.warning('请先选择要导入的文件')
    return
  }

  try {
    importing.value = true
    importProgress.value = 0
    importResult.value = null

    // 模拟文件解析和导入过程
    for (let i = 0; i <= 100; i += 10) {
      importProgress.value = i
      await new Promise(resolve => setTimeout(resolve, 100))
    }

    // 模拟导入结果
    const mockResult = {
      success: 8,
      failed: 2,
      errors: [
        { row: 3, message: '邮箱格式不正确' },
        { row: 7, message: '部门不存在' }
      ]
    }

    importResult.value = mockResult

    // 模拟添加成功导入的用户
    const newUsers = [
      {
        id: Date.now() + 1,
        username: 'wangwu',
        real_name: '王五',
        email: 'wangwu@example.com',
        phone: '13800138005',
        employee_id: 'EMP005',
        department_id: 1,
        department_name: '技术部',
        position: '工程师',
        is_active: true,
        created_at: new Date().toISOString(),
        last_login: null
      },
      {
        id: Date.now() + 2,
        username: 'zhaoliu',
        real_name: '赵六',
        email: 'zhaoliu@example.com',
        phone: '13800138006',
        employee_id: 'EMP006',
        department_id: 2,
        department_name: '生产部',
        position: '技术员',
        is_active: true,
        created_at: new Date().toISOString(),
        last_login: null
      }
    ]

    allUsers.value.unshift(...newUsers)

    if (mockResult.failed === 0) {
      ElMessage.success('用户导入成功')
    } else {
      ElMessage.warning('用户导入完成，部分数据导入失败')
    }
  } catch (error) {
    console.error('导入用户失败:', error)
    ElMessage.error('导入用户失败')
  } finally {
    importing.value = false
  }
}

onMounted(() => {
  loadData()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理表单引用
  if (userFormRef.value) {
    userFormRef.value = null
  }
  if (uploadRef.value) {
    uploadRef.value = null
  }
})
</script>

<style scoped>
.all-users {
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
  flex-direction: column;
  gap: 8px;
  flex: 1;
  max-width: 600px;
}

.header-right {
  flex-shrink: 0;
  margin-left: 32px;
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
  margin: 0;
  color: #909399;
  font-size: 15px;
  line-height: 1.4;
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
  flex-wrap: wrap;
  gap: 8px;
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

/* 分页样式 */
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 统计样式 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  transition: all 0.2s ease;
  min-width: 0; /* 防止内容溢出 */
}

.stat-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card.total {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-color: #93c5fd;
}

.stat-card.active {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-color: #86efac;
}

.stat-card.manager {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #fcd34d;
}

.stat-card.executor {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  border-color: #f9a8d4;
}

.stat-icon {
  margin-right: 12px;
  font-size: 20px;
  color: #374151;
}

.stat-content {
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
  overflow: hidden;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-details {
  border-top: 1px solid #e5e7eb;
  padding-top: 12px;
}

.role-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #f3f4f6;
}

.role-item:last-child {
  border-bottom: none;
}

.role-name {
  font-size: 13px;
  color: #4b5563;
}

.role-count {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 12px;
  min-width: 24px;
  text-align: center;
}

/* 部门分布样式 */
.dept-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dept-stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dept-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dept-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.dept-count {
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
    padding: 20px 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
    min-height: auto;
  }

  .header-left {
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
    width: 100%;
    justify-content: flex-start;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
  }

  .stat-card {
    padding: 10px;
  }

  .stat-value {
    font-size: 18px;
  }

  .stat-label {
    font-size: 11px;
  }

  .role-details {
    margin-top: 12px;
  }
}

/* 对话框样式 */
.user-form {
  padding: 8px 0;
}

.import-content {
  padding: 8px 0;
}

.import-tips {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.import-tips h4 {
  margin: 0 0 12px 0;
  color: #1f2937;
  font-size: 14px;
  font-weight: 600;
}

.import-tips ul {
  margin: 0;
  padding-left: 20px;
  color: #4b5563;
  font-size: 13px;
  line-height: 1.6;
}

.import-tips li {
  margin-bottom: 4px;
}

.import-actions {
  margin-bottom: 20px;
  text-align: center;
}

.import-upload {
  margin-bottom: 20px;
}

.import-progress {
  margin: 20px 0;
}

.import-result {
  margin-top: 20px;
}

.import-errors {
  margin-top: 12px;
  padding: 12px;
  background: #fef2f2;
  border-radius: 6px;
  border: 1px solid #fecaca;
}

.import-errors h5 {
  margin: 0 0 8px 0;
  color: #dc2626;
  font-size: 13px;
  font-weight: 600;
}

.import-errors ul {
  margin: 0;
  padding-left: 16px;
  color: #dc2626;
  font-size: 12px;
}

.import-errors li {
  margin-bottom: 4px;
}

/* 表单项优化 */
:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-select) {
  width: 100%;
}

/* 对话框优化 */
:deep(.el-dialog__header) {
  padding: 20px 20px 10px;
  border-bottom: 1px solid #f1f5f9;
}

:deep(.el-dialog__body) {
  padding: 20px;
}

:deep(.el-dialog__footer) {
  padding: 10px 20px 20px;
  border-top: 1px solid #f1f5f9;
}

/* 上传组件优化 */
:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  border-radius: 8px;
}

:deep(.el-upload__tip) {
  margin-top: 8px;
  color: #6b7280;
  font-size: 12px;
}

/* 进度条优化 */
:deep(.el-progress-bar__outer) {
  border-radius: 10px;
}

:deep(.el-progress-bar__inner) {
  border-radius: 10px;
}
</style>
