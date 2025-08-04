<template>
  <div class="sidebar">
    <div class="sidebar-logo">
      <router-link to="/" class="sidebar-logo-link">
        <img
          v-if="!collapse"
          src="/logo.svg"
          alt="Logo"
          class="sidebar-logo-img"
          @error="handleLogoError"
        >
        <h1 v-if="!collapse" class="sidebar-title">Todo系统</h1>
        <h1 v-else class="sidebar-title-mini">T</h1>
      </router-link>
    </div>
    
    <el-scrollbar class="sidebar-scrollbar">
      <el-menu
        :default-active="activeMenu"
        :collapse="collapse"
        :unique-opened="false"
        :collapse-transition="false"
        mode="vertical"
        background-color="var(--sidebar-bg-color)"
        text-color="var(--sidebar-text-color)"
        active-text-color="var(--sidebar-active-text-color)"
        @select="handleMenuSelect"
      >
        <SidebarItem
          v-for="route in routes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMenu, ElScrollbar } from 'element-plus'
import { useAppStore } from '@/stores/app'
import SidebarItem from './SidebarItem.vue'

const route = useRoute()
const appStore = useAppStore()

// 计算属性
const collapse = computed(() => !appStore.sidebar.opened)
const activeMenu = computed(() => route.path)

// 路由配置
const routes = computed(() => [
  {
    path: '/dashboard',
    name: 'Dashboard',
    meta: { title: '工作台', icon: 'Dashboard' },
    component: () => import('@/views/dashboard/index.vue')
  },
  {
    path: '/tasks',
    name: 'Tasks',
    meta: { title: '任务管理', icon: 'List' },
    children: [
      {
        path: '/tasks/my',
        name: 'MyTasks',
        meta: { title: '我的任务', icon: 'User' }
      },
      {
        path: '/tasks/list',
        name: 'TaskList',
        meta: { title: '任务列表', icon: 'Document' }
      },
      {
        path: '/tasks/create',
        name: 'TaskCreate',
        meta: { title: '创建任务', icon: 'Plus' }
      }
    ]
  },
  {
    path: '/departments',
    name: 'Departments',
    meta: { title: '部门管理', icon: 'OfficeBuilding' }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    meta: { title: '消息通知', icon: 'Bell' }
  },
  {
    path: '/reports',
    name: 'Reports',
    meta: { title: '统计报表', icon: 'DataAnalysis' }
  },
  {
    path: '/settings',
    name: 'Settings',
    meta: { title: '系统设置', icon: 'Setting' },
    children: [
      {
        path: '/settings/profile',
        name: 'Profile',
        meta: { title: '个人资料', icon: 'User' }
      },
      {
        path: '/settings/notifications',
        name: 'NotificationSettings',
        meta: { title: '通知设置', icon: 'Bell' }
      },
      {
        path: '/settings/integrations',
        name: 'Integrations',
        meta: { title: '集成设置', icon: 'Connection' }
      }
    ]
  }
])

// 方法
const handleMenuSelect = (index) => {
  console.log('Menu selected:', index)
}

const handleLogoError = () => {
  console.log('Logo load error')
}
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  background-color: var(--sidebar-bg-color, #304156);
}

.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--sidebar-border-color, #434a50);
  
  .sidebar-logo-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--sidebar-text-color, #bfcbd9);
    
    .sidebar-logo-img {
      width: 32px;
      height: 32px;
      margin-right: 12px;
    }
    
    .sidebar-title {
      font-size: 18px;
      font-weight: 600;
      margin: 0;
      white-space: nowrap;
    }
    
    .sidebar-title-mini {
      font-size: 20px;
      font-weight: 600;
      margin: 0;
    }
  }
}

.sidebar-scrollbar {
  height: calc(100% - 60px);
  
  :deep(.el-scrollbar__view) {
    height: 100%;
  }
}

:deep(.el-menu) {
  border: none;
  height: 100%;
  width: 100% !important;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
  
  &:hover {
    background-color: var(--sidebar-hover-bg-color, #263445) !important;
  }
}

:deep(.el-menu-item.is-active) {
  background-color: var(--sidebar-active-bg-color, #409eff) !important;
}

:deep(.el-sub-menu .el-menu-item) {
  background-color: var(--sidebar-submenu-bg-color, #1f2d3d) !important;
  
  &:hover {
    background-color: var(--sidebar-submenu-hover-bg-color, #001528) !important;
  }
}
</style>
