<template>
  <div class="navbar">
    <div class="navbar-left">
      <!-- 折叠按钮 -->
      <hamburger 
        :is-active="sidebar.opened" 
        class="hamburger-container" 
        @toggle-click="toggleSideBar" 
      />
      
      <!-- 面包屑 -->
      <breadcrumb class="breadcrumb-container" />
    </div>

    <div class="navbar-right">
      <!-- 通知 -->
      <div class="right-menu-item hover-effect" @click="showNotifications">
        <el-badge :value="unreadNotifications" :hidden="unreadNotifications === 0">
          <el-icon :size="18">
            <Bell />
          </el-icon>
        </el-badge>
      </div>

      <!-- 全屏 -->
      <div class="right-menu-item hover-effect" @click="toggleFullscreen">
        <el-icon :size="18">
          <FullScreen v-if="!isFullscreen" />
          <Aim v-else />
        </el-icon>
      </div>

      <!-- 主题切换 -->
      <div class="right-menu-item hover-effect" @click="toggleTheme">
        <el-icon :size="18">
          <Sunny v-if="theme === 'light'" />
          <Moon v-else />
        </el-icon>
      </div>

      <!-- 用户菜单 -->
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img 
            :src="userInfo?.profile?.avatar || defaultAvatar" 
            class="user-avatar"
            :alt="userInfo?.real_name"
          >
          <el-icon class="el-icon-caret-bottom">
            <CaretBottom />
          </el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <router-link to="/settings/profile">
              <el-dropdown-item>
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
            </router-link>
            <router-link to="/settings/notifications">
              <el-dropdown-item>
                <el-icon><Setting /></el-icon>
                通知设置
              </el-dropdown-item>
            </router-link>
            <el-dropdown-item divided @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import Hamburger from './Hamburger.vue'
import Breadcrumb from './Breadcrumb.vue'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 状态
const isFullscreen = ref(false)
const defaultAvatar = '/src/assets/images/default-avatar.png'

// 计算属性
const sidebar = computed(() => appStore.sidebar)
const theme = computed(() => appStore.theme)
const userInfo = computed(() => userStore.userInfo)
const unreadNotifications = computed(() => appStore.unreadNotifications)

// 方法
const toggleSideBar = () => {
  appStore.toggleSidebar()
  appStore.saveSidebarStatus()
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
      isFullscreen.value = false
    }
  }
}

const toggleTheme = () => {
  const newTheme = theme.value === 'light' ? 'dark' : 'light'
  appStore.setTheme(newTheme)
}

const showNotifications = () => {
  router.push('/notifications')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userStore.logoutUser()
    router.push('/login')
  } catch (error) {
    // 用户取消操作
  }
}

// 监听全屏状态变化
document.addEventListener('fullscreenchange', () => {
  isFullscreen.value = !!document.fullscreenElement
})
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: var(--bg-color);
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;

  .navbar-left {
    display: flex;
    align-items: center;
  }

  .navbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    margin-left: 16px;
  }

  .right-menu-item {
    display: inline-block;
    padding: 0 8px;
    height: 100%;
    font-size: 18px;
    color: var(--text-color-regular);
    vertical-align: text-bottom;
    cursor: pointer;
    transition: background 0.3s;

    &.hover-effect {
      &:hover {
        background: rgba(0, 0, 0, 0.025);
      }
    }
  }

  .avatar-container {
    margin-left: 8px;

    .avatar-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      cursor: pointer;

      .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
      }

      .el-icon-caret-bottom {
        margin-left: 4px;
        font-size: 12px;
      }
    }
  }
}
</style>
