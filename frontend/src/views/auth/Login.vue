<template>
  <div class="login-container">
    <div class="login-form">
      <div class="login-header">
        <h2 class="login-title">海南炼化Todo系统</h2>
        <p class="login-subtitle">任务在线分发管理平台</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form-content"
        auto-complete="on"
        label-position="left"
      >
        <el-form-item prop="username">
          <span class="svg-container">
            <el-icon><User /></el-icon>
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="用户名或工号"
            name="username"
            type="text"
            tabindex="1"
            auto-complete="on"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <span class="svg-container">
            <el-icon><Lock /></el-icon>
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            auto-complete="on"
            size="large"
            @keyup.enter="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <el-icon>
              <View v-if="passwordType === 'password'" />
              <Hide v-else />
            </el-icon>
          </span>
        </el-form-item>

        <el-button
          :loading="loading"
          type="primary"
          size="large"
          style="width: 100%; margin-bottom: 30px;"
          @click.prevent="handleLogin"
        >
          登录
        </el-button>

        <div class="login-tips">
          <p>默认账号密码：</p>
          <p>管理员：admin / admin123</p>
          <p>普通用户：user123 / user123</p>
        </div>
      </el-form>
    </div>

    <div class="login-bg">
      <div class="login-bg-content">
        <h3>高效协作，智能管理</h3>
        <p>为海南炼化量身定制的任务管理系统</p>
        <ul class="feature-list">
          <li>
            <el-icon><Check /></el-icon>
            任务在线分发与跟踪
          </li>
          <li>
            <el-icon><Check /></el-icon>
            多级审批流程管理
          </li>
          <li>
            <el-icon><Check /></el-icon>
            石化通消息推送集成
          </li>
          <li>
            <el-icon><Check /></el-icon>
            实时进度监控统计
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const loginFormRef = ref()
const username = ref()
const password = ref()
const passwordType = ref('password')
const loading = ref(false)

const loginForm = reactive({
  username: 'admin',
  password: 'admin123'
})

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名或工号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
})

// 方法
const showPwd = () => {
  if (passwordType.value === 'password') {
    passwordType.value = ''
  } else {
    passwordType.value = 'password'
  }
  nextTick(() => {
    password.value.focus()
  })
}

const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true

      // 添加超时提示
      const timeoutId = setTimeout(() => {
        if (loading.value) {
          ElMessage.warning('登录处理中，请稍候...')
        }
      }, 3000)

      try {
        await userStore.loginUser(loginForm)

        // 清除超时提示
        clearTimeout(timeoutId)

        // 登录成功后跳转
        const redirect = route.query.redirect || '/dashboard'

        // 使用replace而不是push，避免用户通过后退按钮回到登录页
        await router.replace(redirect)
      } catch (error) {
        clearTimeout(timeoutId)
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.error('请检查输入信息')
      return false
    }
  })
}

// 页面加载完成后聚焦到用户名输入框
nextTick(() => {
  if (loginForm.username === '') {
    username.value.focus()
  } else if (loginForm.password === '') {
    password.value.focus()
  }
})
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  display: flex;
}

.login-form {
  flex: 1;
  max-width: 520px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 80px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);

  .login-header {
    text-align: center;
    margin-bottom: 40px;

    .login-title {
      font-size: 32px;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 8px;
    }

    .login-subtitle {
      font-size: 16px;
      color: #7f8c8d;
      margin: 0;
    }
  }

  .login-form-content {
    .el-form-item {
      border: 1px solid #e4e7ed;
      background: #fff;
      border-radius: 8px;
      color: #454545;
      margin-bottom: 24px;
      position: relative;

      &:hover {
        border-color: #c0c4cc;
      }

      &.is-error {
        border-color: #f56c6c;
      }
    }

    .el-input {
      display: inline-block;
      height: 50px;
      width: 85%;

      :deep(.el-input__wrapper) {
        box-shadow: none;
        background: transparent;
        padding-left: 0;
      }

      :deep(input) {
        background: transparent;
        border: 0px;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: #454545;
        height: 50px;
        caret-color: #454545;

        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px #fff inset !important;
          -webkit-text-fill-color: #454545 !important;
        }
      }
    }

    .svg-container {
      padding: 6px 5px 6px 15px;
      color: #889aa4;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
    }

    .show-pwd {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 16px;
      color: #889aa4;
      cursor: pointer;
      user-select: none;
    }
  }

  .login-tips {
    font-size: 14px;
    color: #7f8c8d;
    text-align: center;
    line-height: 1.6;

    p {
      margin: 4px 0;
    }
  }
}

.login-bg {
  flex: 1;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('/src/assets/images/login-bg.svg') no-repeat center center;
    background-size: cover;
    opacity: 0.1;
  }

  .login-bg-content {
    text-align: center;
    z-index: 1;

    h3 {
      font-size: 36px;
      font-weight: 600;
      margin-bottom: 16px;
    }

    p {
      font-size: 18px;
      margin-bottom: 40px;
      opacity: 0.9;
    }

    .feature-list {
      list-style: none;
      padding: 0;
      text-align: left;
      max-width: 300px;

      li {
        display: flex;
        align-items: center;
        margin-bottom: 16px;
        font-size: 16px;

        .el-icon {
          margin-right: 12px;
          color: #67c23a;
          font-size: 18px;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }

  .login-form {
    max-width: none;
    padding: 40px 20px;
  }

  .login-bg {
    min-height: 200px;
    
    .login-bg-content {
      h3 {
        font-size: 24px;
      }
      
      p {
        font-size: 16px;
      }
      
      .feature-list {
        display: none;
      }
    }
  }
}
</style>
