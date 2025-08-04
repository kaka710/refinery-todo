<template>
  <el-dialog
    v-model="visible"
    :title="`用户详情 - ${userDetail?.real_name || '加载中...'}`"
    width="800px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="user-detail-content">
      <template v-if="userDetail">
        <!-- 用户基本信息 -->
        <div class="detail-section">
          <div class="section-header">
            <el-icon><User /></el-icon>
            <span>基本信息</span>
          </div>
          <div class="section-content">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="detail-item">
                  <label>用户名</label>
                  <span>{{ userDetail.username }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>真实姓名</label>
                  <span>{{ userDetail.real_name }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>工号</label>
                  <span>{{ userDetail.employee_id || '未设置' }}</span>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="detail-item">
                  <label>邮箱</label>
                  <span>{{ userDetail.email || '未设置' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>手机号</label>
                  <span>{{ userDetail.phone || '未设置' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>角色</label>
                  <el-tag :type="getRoleTagType(userDetail.role)">
                    {{ getRoleText(userDetail.role) }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 组织信息 -->
        <div class="detail-section">
          <div class="section-header">
            <el-icon><OfficeBuilding /></el-icon>
            <span>组织信息</span>
          </div>
          <div class="section-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>所属部门</label>
                  <span>{{ userDetail.department?.name || '未分配' }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>职位</label>
                  <span>{{ userDetail.profile?.position || '未设置' }}</span>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>办公地点</label>
                  <span>{{ userDetail.profile?.office_location || '未设置' }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>状态</label>
                  <el-tag :type="userDetail.is_active ? 'success' : 'danger'">
                    {{ userDetail.is_active ? '激活' : '禁用' }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 账户信息 -->
        <div class="detail-section">
          <div class="section-header">
            <el-icon><Clock /></el-icon>
            <span>账户信息</span>
          </div>
          <div class="section-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>注册时间</label>
                  <span>{{ formatDateTime(userDetail.date_joined) }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>最后登录</label>
                  <span>{{ userDetail.last_login ? formatDateTime(userDetail.last_login) : '从未登录' }}</span>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 通知设置 -->
        <div class="detail-section" v-if="userDetail.profile">
          <div class="section-header">
            <el-icon><Bell /></el-icon>
            <span>通知设置</span>
          </div>
          <div class="section-content">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="detail-item">
                  <label>邮件通知</label>
                  <el-tag :type="userDetail.profile.email_notifications ? 'success' : 'info'">
                    {{ userDetail.profile.email_notifications ? '开启' : '关闭' }}
                  </el-tag>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>短信通知</label>
                  <el-tag :type="userDetail.profile.sms_notifications ? 'success' : 'info'">
                    {{ userDetail.profile.sms_notifications ? '开启' : '关闭' }}
                  </el-tag>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <label>石化通通知</label>
                  <el-tag :type="userDetail.profile.shihuatong_notifications ? 'success' : 'info'">
                    {{ userDetail.profile.shihuatong_notifications ? '开启' : '关闭' }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </template>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleEdit" v-if="canEdit">
          <el-icon><Edit /></el-icon>
          编辑用户
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { User, OfficeBuilding, Clock, Bell, Edit } from '@element-plus/icons-vue'
import { getUserDetail } from '@/api/auth'
import { useUserStore } from '@/stores/user'
import { formatDateTime } from '@/utils/date'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  userId: {
    type: [Number, String],
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'edit'])

// Store
const userStore = useUserStore()

// Data
const loading = ref(false)
const userDetail = ref(null)

// Computed
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const canEdit = computed(() => {
  return userStore.hasPermission('can_manage_users') || 
         (userStore.userInfo?.id === userDetail.value?.id)
})

// Methods
const loadUserDetail = async () => {
  if (!props.userId) return
  
  loading.value = true
  try {
    const response = await getUserDetail(props.userId)
    userDetail.value = response.data
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败')
  } finally {
    loading.value = false
  }
}

const getRoleText = (role) => {
  const roleMap = {
    'admin': '系统管理员',
    'dept_manager': '部门负责人',
    'prof_manager': '专业负责人',
    'executor': '执行人'
  }
  return roleMap[role] || role
}

const getRoleTagType = (role) => {
  const typeMap = {
    'admin': 'danger',
    'dept_manager': 'warning',
    'prof_manager': 'primary',
    'executor': 'success'
  }
  return typeMap[role] || 'info'
}

const handleClose = () => {
  visible.value = false
  userDetail.value = null
}

const handleEdit = () => {
  emit('edit', userDetail.value)
  handleClose()
}

// Watch
watch(() => props.userId, (newUserId) => {
  if (newUserId && visible.value) {
    loadUserDetail()
  }
})

watch(visible, (newVisible) => {
  if (newVisible && props.userId) {
    loadUserDetail()
  }
})
</script>

<style scoped>
.user-detail-content {
  min-height: 400px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
  font-weight: 600;
  color: #303133;
}

.section-header .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.section-content {
  padding-left: 24px;
}

.detail-item {
  margin-bottom: 16px;
}

.detail-item label {
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.detail-item span {
  display: block;
  color: #303133;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
