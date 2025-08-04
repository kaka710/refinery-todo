<template>
  <div class="app-wrapper" :class="classObj">
    <!-- 移动端遮罩 -->
    <div 
      v-if="device === 'mobile' && sidebar.opened" 
      class="drawer-bg" 
      @click="handleClickOutside"
    />
    
    <!-- 侧边栏 -->
    <Sidebar class="sidebar-container" />
    
    <!-- 主内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="fixed-header">
        <Navbar />
      </div>
      
      <!-- 页面内容 -->
      <AppMain />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import Sidebar from './components/Sidebar/index.vue'
import Navbar from './components/Navbar.vue'
import AppMain from './components/AppMain.vue'

const appStore = useAppStore()

// 计算属性
const sidebar = computed(() => appStore.sidebar)
const device = computed(() => appStore.device)

const classObj = computed(() => {
  return {
    hideSidebar: !sidebar.value.opened,
    openSidebar: sidebar.value.opened,
    withoutAnimation: sidebar.value.withoutAnimation,
    mobile: device.value === 'mobile'
  }
})

// 方法
const handleClickOutside = () => {
  appStore.closeSidebar(false)
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100%;
  width: 100%;

  &.mobile.openSidebar {
    position: fixed;
    top: 0;
  }
}

.drawer-bg {
  background: #000;
  opacity: 0.3;
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
}

.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - 210px);
  transition: width 0.28s;
}

.hideSidebar .fixed-header {
  width: calc(100% - 54px);
}

.mobile .fixed-header {
  width: 100%;
}

.sidebar-container {
  transition: width 0.28s;
  width: 210px !important;
  background-color: var(--bg-color);
  height: 100%;
  position: fixed;
  font-size: 0px;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.hideSidebar .sidebar-container {
  pointer-events: none;
  transition-duration: 0.3s;
  transform: translate3d(-210px, 0, 0);
}

.main-container {
  min-height: 100%;
  transition: margin-left 0.28s;
  margin-left: 210px;
  position: relative;
}

.hideSidebar .main-container {
  margin-left: 54px;
}

.sidebar-container .horizontal-collapse-transition,
.sidebar-container .horizontal-collapse-transition .el-sub-menu__title .el-sub-menu__icon-arrow {
  transition: 0.2s;
}

.sidebar-container .nestable-menu .el-sub-menu > .el-sub-menu__title,
.sidebar-container .el-sub-menu .el-menu-item {
  min-width: 210px !important;
  background-color: var(--bg-color) !important;

  &:hover {
    background-color: var(--primary-color) !important;
  }
}

.mobile .main-container {
  margin-left: 0px;
}

.withoutAnimation {
  .main-container,
  .sidebar-container {
    transition: none;
  }
}
</style>
