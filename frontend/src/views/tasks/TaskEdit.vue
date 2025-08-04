<template>
  <div class="task-edit">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>编辑任务</span>
          <el-button @click="handleBack">返回</el-button>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        style="max-width: 600px"
      >
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入任务标题" />
        </el-form-item>
        
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="form.priority" placeholder="请选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="分配模式" prop="assignment_mode">
          <el-radio-group v-model="form.assignment_mode">
            <el-radio value="one_to_one">一对一分配</el-radio>
            <el-radio value="one_to_many">一对多分配</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="执行部门" prop="department">
          <el-select
            v-model="form.department"
            placeholder="请选择执行部门"
            filterable
            @change="handleDepartmentChange"
            style="width: 100%"
          >
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
          <div class="form-tip">
            <el-text size="small" type="info">
              选择部门后可选择该部门的人员
            </el-text>
          </div>
        </el-form-item>

        <el-form-item label="负责人" prop="primary_assignee">
          <el-select
            v-model="form.primary_assignee"
            placeholder="请先选择执行部门"
            filterable
            :disabled="!form.department"
            @change="handlePrimaryAssigneeChange"
            style="width: 100%"
          >
            <el-option
              v-for="user in departmentUsers"
              :key="user.id"
              :label="`${user.real_name} (${user.employee_id})`"
              :value="user.id"
            />
          </el-select>
          <div class="form-tip">
            <el-text size="small" type="info">
              从所选部门中选择负责人
            </el-text>
          </div>
        </el-form-item>

        <el-form-item
          v-if="form.assignment_mode === 'one_to_many'"
          label="协办部门"
          prop="collaborator_departments"
        >
          <el-select
            v-model="form.collaborator_departments"
            multiple
            placeholder="请选择协办部门"
            filterable
            @change="handleCollaboratorDepartmentsChange"
            style="width: 100%"
            size="large"
          >
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
          <div class="form-tip">
            <el-text size="small" type="info">
              可选择多个部门，然后从各部门中选择协办人
            </el-text>
          </div>
        </el-form-item>

        <el-form-item
          v-if="form.assignment_mode === 'one_to_many' && form.collaborator_departments.length > 0"
          label="协办人"
          prop="collaborators"
        >
          <div class="collaborator-selection">
            <div
              v-for="deptId in form.collaborator_departments"
              :key="deptId"
              class="department-group"
            >
              <div class="department-header">
                <el-tag type="primary" size="small">
                  {{ getDepartmentName(deptId) }}
                </el-tag>
              </div>
              <el-select
                :model-value="getCollaboratorsByDepartment(deptId)"
                @update:model-value="(value) => updateCollaboratorsByDepartment(deptId, value)"
                multiple
                :placeholder="`请选择${getDepartmentName(deptId)}的协办人`"
                filterable
                style="width: 100%; margin-top: 8px;"
                size="large"
              >
                <el-option
                  v-for="user in getAvailableCollaboratorsByDepartment(deptId)"
                  :key="user.id"
                  :label="`${user.real_name} (${user.employee_id})`"
                  :value="user.id"
                />
              </el-select>
            </div>
          </div>
          <div class="form-tip">
            <el-text size="small" type="info">
              按部门分组选择协办人，可从多个部门选择人员
            </el-text>
          </div>
        </el-form-item>
        
        <el-form-item label="截止日期" prop="due_date">
          <el-date-picker
            v-model="form.due_date"
            type="date"
            placeholder="请选择截止日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="预估工时" prop="estimated_hours">
          <el-input-number
            v-model="form.estimated_hours"
            :min="1"
            :max="1000"
            placeholder="请输入预估工时"
            style="width: 100%"
          />
          <div class="form-tip">
            <el-text size="small" type="info">
              单位：小时
            </el-text>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            保存修改
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const submitting = ref(false)
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
  status: '',
  priority: '',
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
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
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

// 模拟任务数据
const mockTask = {
  id: 1,
  title: '完成项目需求分析',
  description: '分析项目需求，编写需求文档，确定技术方案',
  status: 'in_progress',
  priority: 'high',
  assignment_mode: 'one_to_many',
  department: 1, // 生产部
  primary_assignee: 1,
  collaborator_departments: [2, 3], // 技术部、质量部
  collaborators: [4, 7], // 张三(技术部)、李四(质量部)
  due_date: '2024-01-15',
  estimated_hours: 40
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
    // 这里应该调用API获取部门列表
    // const response = await departmentsApi.getDepartments()
    // departments.value = response.data

    // 模拟API调用
    departments.value = mockDepartments
  } catch (error) {
    ElMessage.error('加载部门列表失败')
  }
}

// 加载主部门用户
const loadDepartmentUsers = async (departmentId) => {
  try {
    // 这里应该调用API获取部门用户
    // const response = await departmentsApi.getDepartmentUsers(departmentId)
    // departmentUsers.value = response.data

    // 模拟API调用
    departmentUsers.value = mockUsersByDepartment[departmentId] || []
  } catch (error) {
    ElMessage.error('加载部门用户失败')
  }
}

// 加载协办部门用户
const loadCollaboratorDepartmentUsers = async (departmentId) => {
  try {
    // 这里应该调用API获取部门用户
    // const response = await departmentsApi.getDepartmentUsers(departmentId)
    // collaboratorDepartmentUsers.value[departmentId] = response.data

    // 模拟API调用
    collaboratorDepartmentUsers.value[departmentId] = mockUsersByDepartment[departmentId] || []
  } catch (error) {
    ElMessage.error('加载协办部门用户失败')
  }
}

const loadTask = async () => {
  loading.value = true
  try {
    const taskId = route.params.id

    // 这里应该调用API获取任务详情
    // const response = await tasksApi.getTask(taskId)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 填充表单数据
    Object.assign(form.value, mockTask)

    // 如果有部门信息，加载部门用户
    if (form.value.department) {
      await loadDepartmentUsers(form.value.department)
    }

    // 如果有协办部门信息，加载协办部门用户
    if (form.value.collaborator_departments && form.value.collaborator_departments.length > 0) {
      for (const deptId of form.value.collaborator_departments) {
        await loadCollaboratorDepartmentUsers(deptId)
      }
    }
  } catch (error) {
    ElMessage.error('加载任务详情失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    // 构建提交数据
    const submitData = {
      title: form.value.title,
      description: form.value.description,
      status: form.value.status,
      priority: form.value.priority,
      assignment_mode: form.value.assignment_mode,
      department_id: form.value.department,
      due_date: form.value.due_date,
      estimated_hours: form.value.estimated_hours,
      assignee_ids: [form.value.primary_assignee, ...form.value.collaborators],
      primary_assignee_id: form.value.primary_assignee
    }

    console.log('更新数据:', submitData)

    // 这里应该调用API更新任务
    // await tasksApi.updateTask(route.params.id, submitData)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('任务更新成功')
    router.push(`/tasks/${route.params.id}`)
  } catch (error) {
    if (error !== false) { // 不是表单验证错误
      ElMessage.error('更新任务失败')
    }
  } finally {
    submitting.value = false
  }
}

const handleReset = () => {
  loadTask()
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  loadDepartments()
  loadTask()
})
</script>

<style scoped>
.task-edit {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  margin-top: 4px;
}

.el-radio-group {
  width: 100%;
}

.el-radio {
  margin-right: 20px;
}

/* 协办人选择器样式 */
.el-select .el-tag {
  margin: 2px;
}

/* 协办人分组选择样式 */
.collaborator-selection {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.department-group {
  background: white;
  border-radius: 10px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  margin-bottom: 16px;
}

.department-group:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.department-group:last-child {
  margin-bottom: 0;
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
</style>
