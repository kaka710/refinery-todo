<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="user-edit-content">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="user-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                :disabled="mode === 'edit'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工号" prop="employee_id">
              <el-input v-model="form.employee_id" placeholder="请输入工号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="form.role" placeholder="请选择角色">
                <el-option label="系统管理员" value="admin" />
                <el-option label="部门负责人" value="dept_manager" />
                <el-option label="专业负责人" value="prof_manager" />
                <el-option label="执行人员" value="executor" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department_id">
              <el-select v-model="form.department_id" placeholder="请选择部门">
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
            <el-form-item label="职位" prop="position">
              <el-input v-model="form.position" placeholder="请输入职位" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="状态">
          <el-switch
            v-model="form.is_active"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>

        <template v-if="mode === 'create'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="密码" prop="password">
                <el-input
                  v-model="form.password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="确认密码" prop="confirm_password">
                <el-input
                  v-model="form.confirm_password"
                  type="password"
                  placeholder="请再次输入密码"
                  show-password
                />
              </el-form-item>
            </el-col>
          </el-row>
        </template>
      </el-form>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          {{ saving ? '保存中...' : '保存' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { updateUser, createUser, getUserDetail } from '@/api/auth'
import { departmentsApi } from '@/api/departments'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'create', // 'create' | 'edit'
    validator: (value) => ['create', 'edit'].includes(value)
  },
  userId: {
    type: [Number, String],
    default: null
  },
  departments: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'success'])

// Data
const loading = ref(false)
const saving = ref(false)
const formRef = ref()

// Form data
const form = reactive({
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

// Form rules
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
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
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// Computed
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const dialogTitle = computed(() => {
  return props.mode === 'create' ? '新建用户' : '编辑用户'
})

// Methods
const resetForm = () => {
  Object.assign(form, {
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
  formRef.value?.clearValidate()
}

const loadUserDetail = async () => {
  if (props.mode !== 'edit' || !props.userId) return
  
  loading.value = true
  try {
    const response = await getUserDetail(props.userId)
    const userDetail = response.data
    
    Object.assign(form, {
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
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  try {
    await formRef.value.validate()
    
    saving.value = true
    
    const submitData = {
      username: form.username,
      real_name: form.real_name,
      email: form.email,
      phone: form.phone,
      employee_id: form.employee_id,
      department_id: form.department_id,
      role: form.role,
      is_active: form.is_active
    }
    
    if (form.password) {
      submitData.password = form.password
    }
    
    if (props.mode === 'create') {
      await createUser(submitData)
      ElMessage.success('用户创建成功')
    } else {
      await updateUser(form.id, submitData)
      ElMessage.success('用户更新成功')
    }
    
    emit('success')
    handleClose()
  } catch (error) {
    if (error !== false) {
      console.error('保存用户失败:', error)
      const errorMsg = error.response?.data?.message || error.message || '保存用户失败'
      ElMessage.error(errorMsg)
    }
  } finally {
    saving.value = false
  }
}

const handleClose = () => {
  visible.value = false
  resetForm()
}

// Watch
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    if (props.mode === 'edit') {
      loadUserDetail()
    } else {
      resetForm()
    }
  }
})
</script>

<style scoped>
.user-edit-content {
  min-height: 200px;
}

.user-form {
  padding: 0 20px;
}

.dialog-footer {
  text-align: right;
}
</style>
