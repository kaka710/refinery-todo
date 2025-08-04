<template>
  <div class="profile">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><User /></el-icon>
        个人资料
      </h1>
      <p class="page-subtitle">管理您的个人信息和账户设置</p>
    </div>

    <el-row :gutter="24">
      <!-- 左侧个人信息 -->
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <div class="profile-sections">
          <!-- 基本信息 -->
          <el-card class="profile-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>基本信息</span>
                <el-button
                  v-if="!editMode.basic"
                  type="primary"
                  @click="enableEdit('basic')"
                  size="small"
                >
                  编辑
                </el-button>
                <div v-else class="edit-actions">
                  <el-button size="small" @click="cancelEdit('basic')">取消</el-button>
                  <el-button
                    type="primary"
                    size="small"
                    @click="saveBasicInfo"
                    :loading="saving.basic"
                  >
                    保存
                  </el-button>
                </div>
              </div>
            </template>

            <el-form
              ref="basicFormRef"
              :model="basicForm"
              :rules="basicRules"
              label-width="100px"
              class="profile-form"
            >
              <el-form-item label="真实姓名" prop="real_name">
                <el-input
                  v-model="basicForm.real_name"
                  :disabled="!editMode.basic"
                  placeholder="请输入真实姓名"
                />
              </el-form-item>
              <el-form-item label="工号" prop="employee_id">
                <el-input
                  v-model="basicForm.employee_id"
                  disabled
                  placeholder="工号"
                />
              </el-form-item>
              <el-form-item label="邮箱地址" prop="email">
                <div class="input-with-verification">
                  <el-input
                    v-model="basicForm.email"
                    :disabled="!editMode.basic"
                    placeholder="请输入邮箱地址"
                  />
                  <el-tag
                    v-if="userInfo.email_verified"
                    type="success"
                    size="small"
                    class="verification-tag"
                  >
                    已验证
                  </el-tag>
                  <el-button
                    v-else-if="editMode.basic"
                    size="small"
                    type="primary"
                    link
                    @click="sendEmailVerification"
                  >
                    验证邮箱
                  </el-button>
                </div>
              </el-form-item>
              <el-form-item label="手机号码" prop="phone">
                <div class="input-with-verification">
                  <el-input
                    v-model="basicForm.phone"
                    :disabled="!editMode.basic"
                    placeholder="请输入手机号码"
                  />
                  <el-tag
                    v-if="userInfo.phone_verified"
                    type="success"
                    size="small"
                    class="verification-tag"
                  >
                    已验证
                  </el-tag>
                  <el-button
                    v-else-if="editMode.basic"
                    size="small"
                    type="primary"
                    link
                    @click="sendPhoneVerification"
                  >
                    验证手机
                  </el-button>
                </div>
              </el-form-item>
              <el-form-item label="职位" prop="position">
                <el-input
                  v-model="basicForm.position"
                  :disabled="!editMode.basic"
                  placeholder="请输入职位"
                />
              </el-form-item>
              <el-form-item label="部门" prop="department_name">
                <el-input
                  v-model="basicForm.department_name"
                  disabled
                  placeholder="部门"
                />
              </el-form-item>
              <el-form-item label="办公地点" prop="office_location">
                <el-input
                  v-model="basicForm.office_location"
                  :disabled="!editMode.basic"
                  placeholder="请输入办公地点"
                />
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 密码修改 -->
          <el-card class="profile-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>密码修改</span>
                <el-button
                  v-if="!editMode.password"
                  type="primary"
                  @click="enableEdit('password')"
                  size="small"
                >
                  修改密码
                </el-button>
                <div v-else class="edit-actions">
                  <el-button size="small" @click="cancelEdit('password')">取消</el-button>
                  <el-button
                    type="primary"
                    size="small"
                    @click="changePassword"
                    :loading="saving.password"
                  >
                    确认修改
                  </el-button>
                </div>
              </div>
            </template>

            <div v-if="!editMode.password" class="password-info">
              <p class="info-text">
                <el-icon><Lock /></el-icon>
                为了您的账户安全，建议定期更换密码
              </p>
              <p class="last-change">上次修改时间：{{ formatDate(userInfo.password_changed_at) }}</p>
            </div>

            <el-form
              v-else
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="100px"
              class="profile-form"
            >
              <el-form-item label="当前密码" prop="old_password">
                <el-input
                  v-model="passwordForm.old_password"
                  type="password"
                  placeholder="请输入当前密码"
                  show-password
                />
              </el-form-item>
              <el-form-item label="新密码" prop="new_password">
                <el-input
                  v-model="passwordForm.new_password"
                  type="password"
                  placeholder="请输入新密码"
                  show-password
                />
              </el-form-item>
              <el-form-item label="确认密码" prop="confirm_password">
                <el-input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                />
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 偏好设置 -->
          <el-card class="profile-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>偏好设置</span>
                <el-button
                  v-if="!editMode.preferences"
                  type="primary"
                  @click="enableEdit('preferences')"
                  size="small"
                >
                  编辑
                </el-button>
                <div v-else class="edit-actions">
                  <el-button size="small" @click="cancelEdit('preferences')">取消</el-button>
                  <el-button
                    type="primary"
                    size="small"
                    @click="savePreferences"
                    :loading="saving.preferences"
                  >
                    保存
                  </el-button>
                </div>
              </div>
            </template>

            <el-form
              :model="preferencesForm"
              label-width="120px"
              class="profile-form"
            >
              <el-form-item label="主题设置">
                <el-radio-group v-model="preferencesForm.theme" :disabled="!editMode.preferences">
                  <el-radio value="light">浅色主题</el-radio>
                  <el-radio value="dark">深色主题</el-radio>
                  <el-radio value="auto">跟随系统</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="语言设置">
                <el-select
                  v-model="preferencesForm.language"
                  :disabled="!editMode.preferences"
                  style="width: 200px"
                >
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
              </el-form-item>
              <el-form-item label="通知设置">
                <div class="notification-settings">
                  <el-checkbox
                    v-model="preferencesForm.email_notifications"
                    :disabled="!editMode.preferences"
                  >
                    邮件通知
                  </el-checkbox>
                  <el-checkbox
                    v-model="preferencesForm.sms_notifications"
                    :disabled="!editMode.preferences"
                  >
                    短信通知
                  </el-checkbox>
                  <el-checkbox
                    v-model="preferencesForm.desktop_notifications"
                    :disabled="!editMode.preferences"
                  >
                    桌面通知
                  </el-checkbox>
                </div>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-col>

      <!-- 右侧头像和统计 -->
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <div class="profile-sidebar">
          <!-- 头像卡片 -->
          <el-card class="avatar-card" shadow="never">
            <template #header>
              <span>头像设置</span>
            </template>

            <div class="avatar-section">
              <div class="avatar-container">
                <el-avatar
                  :size="120"
                  :src="userInfo.avatar"
                  class="user-avatar"
                >
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="avatar-overlay">
                  <el-button
                    type="primary"
                    size="small"
                    @click="triggerAvatarUpload"
                    :loading="uploading"
                  >
                    <el-icon><Camera /></el-icon>
                    更换头像
                  </el-button>
                </div>
              </div>

              <input
                ref="avatarInputRef"
                type="file"
                accept="image/*"
                @change="handleAvatarUpload"
                style="display: none"
              />

              <div class="avatar-actions">
                <el-button
                  v-if="userInfo.avatar"
                  size="small"
                  type="danger"
                  @click="deleteAvatar"
                >
                  删除头像
                </el-button>
              </div>

              <div class="avatar-tips">
                <p>支持 JPG、PNG 格式</p>
                <p>文件大小不超过 2MB</p>
                <p>建议尺寸 200x200 像素</p>
              </div>
            </div>
          </el-card>

          <!-- 统计信息 -->
          <el-card class="stats-card" shadow="never">
            <template #header>
              <span>个人统计</span>
            </template>

            <div class="stats-list">
              <div class="stats-item">
                <div class="stats-icon">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stats-info">
                  <div class="stats-number">{{ userStats.total_tasks || 0 }}</div>
                  <div class="stats-label">总任务数</div>
                </div>
              </div>

              <div class="stats-item">
                <div class="stats-icon completed">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="stats-info">
                  <div class="stats-number">{{ userStats.completed_tasks || 0 }}</div>
                  <div class="stats-label">已完成</div>
                </div>
              </div>

              <div class="stats-item">
                <div class="stats-icon rate">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="stats-info">
                  <div class="stats-number">{{ userStats.completion_rate || 0 }}%</div>
                  <div class="stats-label">完成率</div>
                </div>
              </div>

              <div class="stats-item">
                <div class="stats-icon days">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="stats-info">
                  <div class="stats-number">{{ userStats.active_days || 0 }}</div>
                  <div class="stats-label">活跃天数</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 第三方账号绑定 -->
          <el-card class="binding-card" shadow="never">
            <template #header>
              <span>账号绑定</span>
            </template>

            <div class="binding-list">
              <div class="binding-item">
                <div class="binding-info">
                  <el-icon class="binding-icon shihuatong"><Connection /></el-icon>
                  <span>石化通</span>
                </div>
                <div class="binding-action">
                  <el-tag v-if="userInfo.shihuatong_bound" type="success" size="small">
                    已绑定
                  </el-tag>
                  <el-button v-else size="small" type="primary" @click="bindShihuatong">
                    绑定
                  </el-button>
                </div>
              </div>

              <div class="binding-item">
                <div class="binding-info">
                  <el-icon class="binding-icon wechat"><ChatDotRound /></el-icon>
                  <span>微信</span>
                </div>
                <div class="binding-action">
                  <el-tag v-if="userInfo.wechat_bound" type="success" size="small">
                    已绑定
                  </el-tag>
                  <el-button v-else size="small" type="primary" @click="bindWechat">
                    绑定
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Lock, Camera, Document, CircleCheck, TrendCharts, Calendar,
  Connection, ChatDotRound
} from '@element-plus/icons-vue'
import {
  getCurrentUser,
  updateProfile,
  changePassword as changePasswordAPI,
  uploadAvatar as uploadAvatarAPI,
  deleteAvatar as deleteAvatarAPI,
  getUserPreferences,
  updateUserPreferences,
  getUserStats,
  sendEmailVerification as sendEmailVerificationAPI,
  sendPhoneVerification as sendPhoneVerificationAPI,
  bindThirdPartyAccount,
  unbindThirdPartyAccount
} from '@/api/profile'

// 响应式数据
const basicFormRef = ref()
const passwordFormRef = ref()
const avatarInputRef = ref()

const userInfo = ref({})
const userStats = ref({})
const uploading = ref(false)

// 编辑模式
const editMode = reactive({
  basic: false,
  password: false,
  preferences: false
})

// 保存状态
const saving = reactive({
  basic: false,
  password: false,
  preferences: false
})

// 基本信息表单
const basicForm = reactive({
  real_name: '',
  employee_id: '',
  email: '',
  phone: '',
  position: '',
  department_name: '',
  office_location: ''
})

// 密码修改表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 偏好设置表单
const preferencesForm = reactive({
  theme: 'light',
  language: 'zh-CN',
  email_notifications: true,
  sms_notifications: false,
  desktop_notifications: true
})

// 表单验证规则
const basicRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' },
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{6,}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 模拟用户数据
const mockUserInfo = {
  id: 1,
  username: 'zhangsan',
  real_name: '张三',
  employee_id: 'EMP001',
  email: 'zhangsan@example.com',
  phone: '13800138000',
  position: '高级工程师',
  department_name: '技术部',
  office_location: '办公楼A座3层',
  avatar: '',
  email_verified: true,
  phone_verified: false,
  shihuatong_bound: true,
  wechat_bound: false,
  password_changed_at: '2024-01-01T00:00:00Z',
  created_at: '2023-06-01T00:00:00Z'
}

const mockUserStats = {
  total_tasks: 156,
  completed_tasks: 98,
  completion_rate: 62.8,
  active_days: 245
}

const mockPreferences = {
  theme: 'light',
  language: 'zh-CN',
  email_notifications: true,
  sms_notifications: false,
  desktop_notifications: true
}

// 方法
const loadUserInfo = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    userInfo.value = mockUserInfo

    // 填充表单数据
    Object.assign(basicForm, {
      real_name: userInfo.value.real_name,
      employee_id: userInfo.value.employee_id,
      email: userInfo.value.email,
      phone: userInfo.value.phone,
      position: userInfo.value.position,
      department_name: userInfo.value.department_name,
      office_location: userInfo.value.office_location
    })
  } catch (error) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  }
}

const loadUserStats = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 200))
    userStats.value = mockUserStats
  } catch (error) {
    console.error('加载用户统计失败:', error)
  }
}

const loadPreferences = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 250))
    Object.assign(preferencesForm, mockPreferences)
  } catch (error) {
    console.error('加载偏好设置失败:', error)
  }
}

// 编辑模式控制
const enableEdit = (section) => {
  editMode[section] = true

  if (section === 'password') {
    // 清空密码表单
    Object.assign(passwordForm, {
      old_password: '',
      new_password: '',
      confirm_password: ''
    })
  }
}

const cancelEdit = (section) => {
  editMode[section] = false

  if (section === 'basic') {
    // 恢复原始数据
    Object.assign(basicForm, {
      real_name: userInfo.value.real_name,
      employee_id: userInfo.value.employee_id,
      email: userInfo.value.email,
      phone: userInfo.value.phone,
      position: userInfo.value.position,
      department_name: userInfo.value.department_name,
      office_location: userInfo.value.office_location
    })
  } else if (section === 'password') {
    // 清空密码表单
    Object.assign(passwordForm, {
      old_password: '',
      new_password: '',
      confirm_password: ''
    })
  } else if (section === 'preferences') {
    // 恢复偏好设置
    loadPreferences()
  }
}

// 保存基本信息
const saveBasicInfo = async () => {
  try {
    await basicFormRef.value.validate()

    saving.basic = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 更新用户信息
    Object.assign(userInfo.value, {
      real_name: basicForm.real_name,
      email: basicForm.email,
      phone: basicForm.phone,
      position: basicForm.position,
      office_location: basicForm.office_location
    })

    editMode.basic = false
    ElMessage.success('基本信息保存成功')
  } catch (error) {
    if (error !== false) { // 不是表单验证错误
      console.error('保存基本信息失败:', error)
      ElMessage.error('保存基本信息失败')
    }
  } finally {
    saving.basic = false
  }
}

// 修改密码
const changePassword = async () => {
  try {
    await passwordFormRef.value.validate()

    saving.password = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1500))

    // 更新密码修改时间
    userInfo.value.password_changed_at = new Date().toISOString()

    editMode.password = false
    ElMessage.success('密码修改成功')
  } catch (error) {
    if (error !== false) { // 不是表单验证错误
      console.error('修改密码失败:', error)
      ElMessage.error('修改密码失败')
    }
  } finally {
    saving.password = false
  }
}

// 保存偏好设置
const savePreferences = async () => {
  try {
    saving.preferences = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))

    editMode.preferences = false
    ElMessage.success('偏好设置保存成功')
  } catch (error) {
    console.error('保存偏好设置失败:', error)
    ElMessage.error('保存偏好设置失败')
  } finally {
    saving.preferences = false
  }
}

// 头像上传
const triggerAvatarUpload = () => {
  avatarInputRef.value.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }

  // 验证文件大小 (2MB)
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }

  try {
    uploading.value = true

    // 模拟上传
    await new Promise(resolve => setTimeout(resolve, 2000))

    // 创建预览URL
    const avatarUrl = URL.createObjectURL(file)
    userInfo.value.avatar = avatarUrl

    ElMessage.success('头像上传成功')
  } catch (error) {
    console.error('头像上传失败:', error)
    ElMessage.error('头像上传失败')
  } finally {
    uploading.value = false
    // 清空文件输入
    event.target.value = ''
  }
}

const deleteAvatar = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除当前头像吗？',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    userInfo.value.avatar = ''
    ElMessage.success('头像删除成功')
  } catch {
    // 用户取消删除
  }
}

// 邮箱验证
const sendEmailVerification = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('验证邮件已发送，请查收')
  } catch (error) {
    console.error('发送验证邮件失败:', error)
    ElMessage.error('发送验证邮件失败')
  }
}

// 手机验证
const sendPhoneVerification = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('验证短信已发送')
  } catch (error) {
    console.error('发送验证短信失败:', error)
    ElMessage.error('发送验证短信失败')
  }
}

// 第三方账号绑定
const bindShihuatong = async () => {
  try {
    ElMessage.info('正在跳转到石化通授权页面...')

    // 模拟绑定流程
    await new Promise(resolve => setTimeout(resolve, 2000))

    userInfo.value.shihuatong_bound = true
    ElMessage.success('石化通账号绑定成功')
  } catch (error) {
    console.error('绑定石化通失败:', error)
    ElMessage.error('绑定石化通失败')
  }
}

const bindWechat = async () => {
  try {
    ElMessage.info('正在生成微信绑定二维码...')

    // 模拟绑定流程
    await new Promise(resolve => setTimeout(resolve, 2000))

    userInfo.value.wechat_bound = true
    ElMessage.success('微信账号绑定成功')
  } catch (error) {
    console.error('绑定微信失败:', error)
    ElMessage.error('绑定微信失败')
  }
}

// 工具方法
const formatDate = (dateString) => {
  if (!dateString) return '未设置'

  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 生命周期
onMounted(() => {
  loadUserInfo()
  loadUserStats()
  loadPreferences()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理可能的定时器或事件监听器
  if (avatarInputRef.value) {
    avatarInputRef.value = null
  }
})
</script>

<style scoped>
.profile {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

/* 卡片样式 */
.profile-card,
.avatar-card,
.stats-card,
.binding-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1f2937;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

/* 表单样式 */
.profile-form {
  padding: 8px 0;
}

.input-with-verification {
  display: flex;
  align-items: center;
  gap: 8px;
}

.verification-tag {
  flex-shrink: 0;
}

.notification-settings {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 密码信息 */
.password-info {
  padding: 20px 0;
}

.info-text {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px 0;
  color: #4b5563;
  font-size: 14px;
}

.last-change {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

/* 头像部分 */
.avatar-section {
  text-align: center;
  padding: 16px 0;
}

.avatar-container {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.user-avatar {
  border: 3px solid #e5e7eb;
  transition: all 0.3s ease;
}

.avatar-overlay {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.avatar-container:hover .user-avatar {
  border-color: #3b82f6;
}

.avatar-actions {
  margin-bottom: 16px;
}

.avatar-tips {
  color: #6b7280;
  font-size: 12px;
  line-height: 1.5;
}

.avatar-tips p {
  margin: 4px 0;
}

/* 统计信息 */
.stats-list {
  padding: 8px 0;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.stats-item:last-child {
  border-bottom: none;
}

.stats-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.stats-icon.completed {
  background: linear-gradient(135deg, #10b981, #047857);
}

.stats-icon.rate {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.stats-icon.days {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stats-label {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}

/* 账号绑定 */
.binding-list {
  padding: 8px 0;
}

.binding-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.binding-item:last-child {
  border-bottom: none;
}

.binding-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.binding-icon {
  font-size: 20px;
}

.binding-icon.shihuatong {
  color: #1890ff;
}

.binding-icon.wechat {
  color: #07c160;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile {
    padding: 16px;
  }

  .profile-sections {
    margin-bottom: 24px;
  }

  .card-header {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }

  .edit-actions {
    justify-content: flex-end;
  }

  .input-with-verification {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .notification-settings {
    gap: 12px;
  }

  .stats-item {
    padding: 16px 0;
  }

  .binding-item {
    padding: 16px 0;
  }
}

/* 表单项优化 */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

:deep(.el-checkbox) {
  margin-right: 0;
}

/* 按钮样式 */
:deep(.el-button--small) {
  padding: 6px 12px;
  font-size: 13px;
}

/* 标签样式 */
:deep(.el-tag--small) {
  font-size: 11px;
  padding: 2px 6px;
}
</style>
