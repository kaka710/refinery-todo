<template>
  <div class="task-create">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><Plus /></el-icon>
            创建任务
          </h1>
          <p class="page-subtitle">填写任务信息，分配给相关人员</p>
        </div>
        <div class="header-right">
          <el-button @click="handleBack" size="large">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧表单区域 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <el-card class="form-card" shadow="never">
            <template #header>
              <div class="form-card-header">
                <el-icon><Document /></el-icon>
                <span>任务信息</span>
              </div>
            </template>

            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-width="120px"
              label-position="left"
              class="task-form"
            >
              <!-- 基本信息分组 -->
              <div class="form-section">
                <div class="section-title">
                  <el-icon><Edit /></el-icon>
                  <span>基本信息</span>
                </div>

                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="任务标题" prop="title">
                      <el-input
                        v-model="form.title"
                        placeholder="请输入任务标题"
                        size="large"
                        clearable
                      />
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="任务描述" prop="description">
                      <el-input
                        v-model="form.description"
                        type="textarea"
                        :rows="4"
                        placeholder="请详细描述任务内容、要求和目标"
                        show-word-limit
                        maxlength="500"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="16">
                  <el-col :xs="24" :sm="12" :md="12">
                    <el-form-item label="优先级" prop="priority">
                      <el-select v-model="form.priority" placeholder="请选择优先级" style="width: 100%">
                        <el-option label="🟢 低" value="low" />
                        <el-option label="🟡 中" value="medium" />
                        <el-option label="🟠 高" value="high" />
                        <el-option label="🔴 紧急" value="urgent" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12" :md="12">
                    <el-form-item label="预估工时" prop="estimated_hours">
                      <el-input-number
                        v-model="form.estimated_hours"
                        :min="1"
                        :max="1000"
                        placeholder="预估工时"
                        style="width: 100%"
                      />
                      <div class="form-tip">
                        <el-text size="small" type="info">单位：小时</el-text>
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="截止日期" prop="due_date">
                      <el-date-picker
                        v-model="form.due_date"
                        type="datetime"
                        placeholder="请选择截止日期和时间"
                        style="width: 100%"
                        format="YYYY-MM-DD HH:mm"
                        value-format="YYYY-MM-DD HH:mm:ss"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
        
              <!-- 分配信息分组 -->
              <div class="form-section">
                <div class="section-title">
                  <el-icon><User /></el-icon>
                  <span>分配信息</span>
                </div>

                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="分配模式" prop="assignment_mode">
                      <el-radio-group v-model="form.assignment_mode" size="large">
                        <el-radio-button value="one_to_one">
                          <el-icon><User /></el-icon>
                          一对一分配
                        </el-radio-button>
                        <el-radio-button value="one_to_many">
                          <el-icon><UserFilled /></el-icon>
                          一对多分配
                        </el-radio-button>
                      </el-radio-group>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="16">
                  <el-col :xs="24" :sm="24" :md="12">
                    <el-form-item label="执行部门" prop="department">
                      <el-select
                        v-model="form.department"
                        placeholder="请选择执行部门"
                        filterable
                        @change="handleDepartmentChange"
                        style="width: 100%"
                        size="large"
                      >
                        <!-- 直接硬编码选项进行测试 -->
                        <el-option label="生产部" value="1">
                          <span style="float: left">生产部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">PROD</span>
                        </el-option>
                        <el-option label="技术部" value="2">
                          <span style="float: left">技术部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">TECH</span>
                        </el-option>
                        <el-option label="质量部" value="3">
                          <span style="float: left">质量部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">QC</span>
                        </el-option>
                        <el-option label="安全部" value="4">
                          <span style="float: left">安全部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">SAFE</span>
                        </el-option>
                        <el-option label="设备部" value="5">
                          <span style="float: left">设备部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">EQUIP</span>
                        </el-option>
                      </el-select>
                      <div class="form-tip">
                        <el-text size="small" type="info">
                          选择部门后可选择该部门的人员
                        </el-text>
                      </div>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="24" :md="12">
                    <el-form-item label="负责人" prop="primary_assignee">
                      <el-select
                        v-model="form.primary_assignee"
                        placeholder="请先选择执行部门"
                        filterable
                        :disabled="!form.department"
                        @change="handlePrimaryAssigneeChange"
                        style="width: 100%"
                        size="large"
                      >
                        <el-option
                          v-for="user in departmentUsers"
                          :key="user.id"
                          :label="`${user.real_name} (${user.employee_id})`"
                          :value="user.id"
                        >
                          <div class="user-option">
                            <span class="user-name">{{ user.real_name }}</span>
                            <span class="user-id">{{ user.employee_id }}</span>
                          </div>
                        </el-option>
                      </el-select>
                      <div class="form-tip">
                        <el-text size="small" type="info">
                          从所选部门中选择负责人
                        </el-text>
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>

              <!-- 协办信息分组 -->
              <div v-if="form.assignment_mode === 'one_to_many'" class="form-section">
                <div class="section-title">
                  <el-icon><UserFilled /></el-icon>
                  <span>协办信息</span>
                </div>

                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="协办部门" prop="collaborator_departments">
                      <el-select
                        v-model="form.collaborator_departments"
                        multiple
                        placeholder="请选择协办部门"
                        filterable
                        @change="handleCollaboratorDepartmentsChange"
                        style="width: 100%"
                        size="large"
                      >
                        <!-- 直接硬编码选项进行测试 -->
                        <el-option label="生产部" value="1">
                          <span style="float: left">生产部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">PROD</span>
                        </el-option>
                        <el-option label="技术部" value="2">
                          <span style="float: left">技术部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">TECH</span>
                        </el-option>
                        <el-option label="质量部" value="3">
                          <span style="float: left">质量部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">QC</span>
                        </el-option>
                        <el-option label="安全部" value="4">
                          <span style="float: left">安全部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">SAFE</span>
                        </el-option>
                        <el-option label="设备部" value="5">
                          <span style="float: left">设备部</span>
                          <span style="float: right; color: #8492a6; font-size: 13px">EQUIP</span>
                        </el-option>
                      </el-select>
                      <div class="form-tip">
                        <el-text size="small" type="info">
                          可选择多个部门，然后从各部门中选择协办人
                        </el-text>
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row v-if="form.collaborator_departments.length > 0" :gutter="16">
                  <el-col :span="24">
                    <el-form-item label="协办人" prop="collaborators">
                      <div class="collaborator-selection">
                        <el-row :gutter="16">
                          <el-col
                            v-for="deptId in form.collaborator_departments"
                            :key="deptId"
                            :xs="24"
                            :sm="24"
                            :md="12"
                            :lg="8"
                            class="department-col"
                          >
                            <div class="department-group">
                              <div class="department-header">
                                <el-tag type="primary" size="default" effect="dark">
                                  <el-icon><OfficeBuilding /></el-icon>
                                  {{ getDepartmentName(deptId) }}
                                </el-tag>
                              </div>
                              <el-select
                                :model-value="getCollaboratorsByDepartment(deptId)"
                                @update:model-value="(value) => updateCollaboratorsByDepartment(deptId, value)"
                                multiple
                                :placeholder="`选择${getDepartmentName(deptId)}协办人`"
                                filterable
                                style="width: 100%"
                                size="large"
                              >
                                <el-option
                                  v-for="user in getAvailableCollaboratorsByDepartment(deptId)"
                                  :key="user.id"
                                  :label="`${user.real_name} (${user.employee_id})`"
                                  :value="user.id"
                                >
                                  <div class="user-option">
                                    <span class="user-name">{{ user.real_name }}</span>
                                    <span class="user-id">{{ user.employee_id }}</span>
                                  </div>
                                </el-option>
                              </el-select>
                            </div>
                          </el-col>
                        </el-row>
                      </div>
                      <div class="form-tip">
                        <el-text size="small" type="info">
                          按部门分组选择协办人，可从多个部门选择人员
                        </el-text>
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>

              <!-- 表单操作区域 -->
              <div class="form-actions">
                <el-row :gutter="16">
                  <el-col :span="24">
                    <el-button
                      type="primary"
                      @click="handleSubmit"
                      :loading="loading"
                      size="large"
                      style="width: 200px"
                    >
                      <el-icon><Check /></el-icon>
                      创建任务
                    </el-button>
                    <el-button @click="handleBack" size="large" style="margin-left: 16px">
                      <el-icon><Close /></el-icon>
                      取消
                    </el-button>
                  </el-col>
                </el-row>
              </div>
            </el-form>
          </el-card>
        </el-col>

        <!-- 右侧信息面板 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <div class="info-panels">
            <!-- 任务预览 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><View /></el-icon>
                  <span>任务预览</span>
                </div>
              </template>

              <div class="task-preview">
                <div class="preview-item">
                  <label>任务标题：</label>
                  <span>{{ form.title || '未填写' }}</span>
                </div>
                <div class="preview-item">
                  <label>优先级：</label>
                  <el-tag
                    :type="getPriorityType(form.priority)"
                    size="small"
                  >
                    {{ getPriorityText(form.priority) }}
                  </el-tag>
                </div>
                <div class="preview-item">
                  <label>分配模式：</label>
                  <span>{{ form.assignment_mode === 'one_to_one' ? '一对一分配' : '一对多分配' }}</span>
                </div>
                <div class="preview-item" v-if="form.department">
                  <label>执行部门：</label>
                  <span>{{ getDepartmentName(form.department) }}</span>
                </div>
                <div class="preview-item" v-if="form.primary_assignee">
                  <label>负责人：</label>
                  <span>{{ getPrimaryAssigneeName() }}</span>
                </div>
                <div class="preview-item" v-if="form.collaborator_departments.length > 0">
                  <label>协办部门：</label>
                  <div class="collaborator-dept-tags">
                    <el-tag
                      v-for="deptId in form.collaborator_departments"
                      :key="deptId"
                      size="small"
                      style="margin: 2px"
                    >
                      {{ getDepartmentName(deptId) }}
                    </el-tag>
                  </div>
                </div>
                <div class="preview-item" v-if="form.collaborators.length > 0">
                  <label>协办人数：</label>
                  <span>{{ form.collaborators.length }} 人</span>
                </div>
                <div class="preview-item" v-if="form.estimated_hours">
                  <label>预估工时：</label>
                  <span>{{ form.estimated_hours }} 小时</span>
                </div>
                <div class="preview-item" v-if="form.due_date">
                  <label>截止时间：</label>
                  <span>{{ form.due_date }}</span>
                </div>
              </div>
            </el-card>

            <!-- 操作提示 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="info-card-header">
                  <el-icon><InfoFilled /></el-icon>
                  <span>操作提示</span>
                </div>
              </template>

              <div class="tips-content">
                <el-steps direction="vertical" :active="getCurrentStep()" finish-status="success">
                  <el-step title="填写基本信息" description="任务标题、描述、优先级等" />
                  <el-step title="选择分配模式" description="一对一或一对多分配" />
                  <el-step title="选择执行部门" description="任务的主要执行部门" />
                  <el-step title="选择负责人" description="从执行部门中选择负责人" />
                  <el-step
                    v-if="form.assignment_mode === 'one_to_many'"
                    title="选择协办部门"
                    description="可选择多个协办部门"
                  />
                  <el-step
                    v-if="form.assignment_mode === 'one_to_many'"
                    title="选择协办人"
                    description="从各协办部门选择人员"
                  />
                  <el-step title="完成创建" description="检查信息并提交" />
                </el-steps>
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
import { ElMessage } from 'element-plus'
import {
  Plus, ArrowLeft, Document, Edit, User, UserFilled,
  OfficeBuilding, Check, Close, View, InfoFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const departments = ref([])
const departmentUsers = ref([])
const collaboratorDepartmentUsers = ref({}) // 存储各协办部门的用户数据

// 模拟部门数据
const mockDepartments = [
  { id: 1, name: '生产部', code: 'PROD', description: '负责生产运营' },
  { id: 2, name: '技术部', code: 'TECH', description: '负责技术研发' },
  { id: 3, name: '质量部', code: 'QC', description: '负责质量管控' },
  { id: 4, name: '安全部', code: 'SAFE', description: '负责安全管理' },
  { id: 5, name: '设备部', code: 'EQUIP', description: '负责设备维护' }
]

// 模拟用户数据（按部门分组）
const mockUsersByDepartment = {
  1: [ // 生产部
    { id: 1, employee_id: 'P001', real_name: '顾志华', role: 'executor', department_name: '生产部' },
    { id: 2, employee_id: 'P002', real_name: '张生产', role: 'executor', department_name: '生产部' },
    { id: 3, employee_id: 'P003', real_name: '李生产', role: 'executor', department_name: '生产部' }
  ],
  2: [ // 技术部
    { id: 4, employee_id: 'T001', real_name: '张三', role: 'executor', department_name: '技术部' },
    { id: 5, employee_id: 'T002', real_name: '王技术', role: 'executor', department_name: '技术部' },
    { id: 6, employee_id: 'T003', real_name: '赵技术', role: 'executor', department_name: '技术部' }
  ],
  3: [ // 质量部
    { id: 7, employee_id: 'Q001', real_name: '李四', role: 'executor', department_name: '质量部' },
    { id: 8, employee_id: 'Q002', real_name: '陈质量', role: 'executor', department_name: '质量部' }
  ],
  4: [ // 安全部
    { id: 9, employee_id: 'S001', real_name: '王五', role: 'executor', department_name: '安全部' },
    { id: 10, employee_id: 'S002', real_name: '刘安全', role: 'executor', department_name: '安全部' }
  ],
  5: [ // 设备部
    { id: 11, employee_id: 'E001', real_name: '赵六', role: 'executor', department_name: '设备部' },
    { id: 12, employee_id: 'E002', real_name: '孙设备', role: 'executor', department_name: '设备部' }
  ]
}

const form = ref({
  title: '',
  description: '',
  priority: 'medium',
  assignment_mode: 'one_to_one',
  department: '',
  primary_assignee: '',
  collaborator_departments: [],
  collaborators: [],
  due_date: '',
  estimated_hours: null
})

const rules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  assignment_mode: [
    { required: true, message: '请选择分配模式', trigger: 'change' }
  ],
  department: [
    { required: true, message: '请选择执行部门', trigger: 'change' }
  ],
  primary_assignee: [
    { required: true, message: '请选择负责人', trigger: 'change' }
  ],
  due_date: [
    { required: true, message: '请选择截止日期', trigger: 'change' }
  ]
}

// 获取部门名称
const getDepartmentName = (deptId) => {
  const dept = departments.value.find(d => d.id === deptId)
  return dept ? dept.name : ''
}

// 获取指定部门的协办人
const getCollaboratorsByDepartment = (deptId) => {
  return form.value.collaborators.filter(userId => {
    const users = collaboratorDepartmentUsers.value[deptId] || []
    return users.some(user => user.id === userId)
  })
}

// 更新指定部门的协办人
const updateCollaboratorsByDepartment = (deptId, userIds) => {
  // 移除该部门原有的协办人
  const otherDeptUsers = form.value.collaborators.filter(userId => {
    const users = collaboratorDepartmentUsers.value[deptId] || []
    return !users.some(user => user.id === userId)
  })

  // 添加新选择的协办人
  form.value.collaborators = [...otherDeptUsers, ...userIds]
}

// 获取指定部门可选的协办人（排除负责人）
const getAvailableCollaboratorsByDepartment = (deptId) => {
  const users = collaboratorDepartmentUsers.value[deptId] || []
  return users.filter(user => user.id !== form.value.primary_assignee)
}

// 处理主部门变更
const handleDepartmentChange = async (departmentId) => {
  // 清空人员选择
  form.value.primary_assignee = ''
  form.value.collaborators = []
  form.value.collaborator_departments = []

  if (departmentId) {
    await loadDepartmentUsers(departmentId)
  } else {
    departmentUsers.value = []
  }
}

// 处理协办部门变更
const handleCollaboratorDepartmentsChange = async (departmentIds) => {
  // 清空协办人选择
  form.value.collaborators = []

  // 加载新选择部门的用户数据
  for (const deptId of departmentIds) {
    if (!collaboratorDepartmentUsers.value[deptId]) {
      await loadCollaboratorDepartmentUsers(deptId)
    }
  }

  // 移除未选择部门的用户数据
  const newCollaboratorDepartmentUsers = {}
  for (const deptId of departmentIds) {
    if (collaboratorDepartmentUsers.value[deptId]) {
      newCollaboratorDepartmentUsers[deptId] = collaboratorDepartmentUsers.value[deptId]
    }
  }
  collaboratorDepartmentUsers.value = newCollaboratorDepartmentUsers
}

// 处理负责人变更
const handlePrimaryAssigneeChange = (assigneeId) => {
  // 如果负责人在协办人列表中，则移除
  if (form.value.collaborators.includes(assigneeId)) {
    form.value.collaborators = form.value.collaborators.filter(id => id !== assigneeId)
  }
}

// 加载部门列表
const loadDepartments = async () => {
  try {
    console.log('=== 开始加载部门列表 ===')
    console.log('mockDepartments:', mockDepartments)
    console.log('departments.value 赋值前:', departments.value)

    // 这里应该调用API获取部门列表
    // const response = await departmentsApi.getDepartments()
    // departments.value = response.data

    // 模拟API调用
    departments.value = mockDepartments

    console.log('departments.value 赋值后:', departments.value)
    console.log('departments.value.length:', departments.value.length)
    console.log('=== 部门列表加载完成 ===')
  } catch (error) {
    console.error('加载部门列表失败:', error)
    ElMessage.error('加载部门列表失败')
  }
}

// 加载主部门用户
const loadDepartmentUsers = async (departmentId) => {
  try {
    // 这里应该调用API获取部门用户
    // const response = await departmentsApi.getDepartmentUsers(departmentId)
    // departmentUsers.value = response.data

    // 模拟API调用 - 确保数据类型匹配
    const deptId = parseInt(departmentId) || departmentId
    departmentUsers.value = mockUsersByDepartment[deptId] || []
    console.log('加载部门用户:', deptId, departmentUsers.value)
  } catch (error) {
    console.error('加载部门用户失败:', error)
    ElMessage.error('加载部门用户失败')
  }
}

// 加载协办部门用户
const loadCollaboratorDepartmentUsers = async (departmentId) => {
  try {
    // 这里应该调用API获取部门用户
    // const response = await departmentsApi.getDepartmentUsers(departmentId)
    // collaboratorDepartmentUsers.value[departmentId] = response.data

    // 模拟API调用 - 确保数据类型匹配
    const deptId = parseInt(departmentId) || departmentId
    collaboratorDepartmentUsers.value[departmentId] = mockUsersByDepartment[deptId] || []
    console.log('加载协办部门用户:', deptId, collaboratorDepartmentUsers.value[departmentId])
  } catch (error) {
    console.error('加载协办部门用户失败:', error)
    ElMessage.error('加载协办部门用户失败')
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    loading.value = true

    // 构建提交数据
    const submitData = {
      title: form.value.title,
      description: form.value.description,
      priority: form.value.priority,
      assignment_mode: form.value.assignment_mode,
      department_id: form.value.department,
      due_date: form.value.due_date,
      estimated_hours: form.value.estimated_hours,
      assignee_ids: [form.value.primary_assignee, ...form.value.collaborators],
      primary_assignee_id: form.value.primary_assignee
    }

    console.log('提交数据:', submitData)

    // 这里应该调用API创建任务
    // await tasksApi.createTask(submitData)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('任务创建成功')
    router.push('/tasks')
  } catch (error) {
    if (error !== false) { // 不是表单验证错误
      ElMessage.error('创建任务失败')
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  formRef.value.resetFields()
}

const handleBack = () => {
  router.back()
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const types = {
    low: 'success',
    medium: 'warning',
    high: 'danger',
    urgent: 'danger'
  }
  return types[priority] || 'info'
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const texts = {
    low: '🟢 低',
    medium: '🟡 中',
    high: '🟠 高',
    urgent: '🔴 紧急'
  }
  return texts[priority] || '未设置'
}

// 获取负责人姓名
const getPrimaryAssigneeName = () => {
  if (!form.value.primary_assignee) return '未选择'
  const user = departmentUsers.value.find(u => u.id === form.value.primary_assignee)
  return user ? `${user.real_name} (${user.employee_id})` : '未找到'
}

// 获取当前步骤
const getCurrentStep = () => {
  if (!form.value.title) return 0
  if (!form.value.assignment_mode) return 1
  if (!form.value.department) return 2
  if (!form.value.primary_assignee) return 3
  if (form.value.assignment_mode === 'one_to_many') {
    if (form.value.collaborator_departments.length === 0) return 4
    if (form.value.collaborators.length === 0) return 5
    return 6
  }
  return 4
}

// 组件挂载时加载部门列表
onMounted(() => {
  console.log('onMounted 执行')

  // 直接硬编码测试
  departments.value = [
    { id: 1, name: '生产部', code: 'PROD' },
    { id: 2, name: '技术部', code: 'TECH' }
  ]
  console.log('硬编码后 departments.value:', departments.value)

  // 然后调用正常的加载函数
  loadDepartments()
})
</script>

<style scoped>
.task-create {
  min-height: 100vh;
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

.header-left {
  flex: 1;
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

.header-right {
  flex-shrink: 0;
}

/* 主要内容区域 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px 32px;
}

/* 表单卡片样式 */
.form-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 表单样式 */
.task-form {
  padding: 8px 0;
}

.form-section {
  margin-bottom: 32px;
  padding: 24px;
  background: #fafbfc;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #409eff;
}

.form-tip {
  margin-top: 6px;
}

.form-actions {
  margin-top: 40px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  text-align: center;
}

/* 用户选项样式 */
.user-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-weight: 500;
}

.user-id {
  color: #909399;
  font-size: 12px;
}

/* 协办人选择样式 */
.collaborator-selection {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.department-col {
  margin-bottom: 20px;
}

.department-group {
  background: white;
  border-radius: 10px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.department-group:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.department-header {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.department-header .el-tag {
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 8px;
}

.department-header .el-icon {
  font-size: 14px;
}

.department-header .el-tag {
  font-weight: 500;
}

/* 右侧信息面板 */
.info-panels {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

/* 任务预览样式 */
.task-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preview-item label {
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.preview-item span {
  font-size: 14px;
  color: #303133;
}

.collaborator-dept-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 操作提示样式 */
.tips-content {
  padding: 8px 0;
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

  .form-section {
    padding: 16px;
    margin-bottom: 20px;
  }

  .page-title {
    font-size: 24px;
  }
}

/* Element Plus 组件样式覆盖 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 6px;
}

/* 多选标签样式优化 */
:deep(.el-select .el-tag) {
  margin: 2px 4px 2px 0;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.el-select .el-tag.el-tag--info) {
  background-color: #f0f9ff;
  border-color: #0ea5e9;
  color: #0369a1;
}

:deep(.el-select .el-tag .el-tag__close) {
  color: #64748b;
  font-size: 12px;
}

:deep(.el-select .el-tag .el-tag__close:hover) {
  background-color: #ef4444;
  color: white;
}

:deep(.el-button) {
  border-radius: 6px;
  font-weight: 500;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
