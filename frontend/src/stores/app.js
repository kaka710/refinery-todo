import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 状态
  const sidebar = ref({
    opened: true,
    withoutAnimation: false
  })
  
  const device = ref('desktop')
  const size = ref('default')
  const theme = ref('light')
  const language = ref('zh-cn')
  
  // 页面加载状态
  const loading = ref(false)
  
  // 通知相关
  const unreadNotifications = ref(0)

  // 方法
  const toggleSidebar = () => {
    sidebar.value.opened = !sidebar.value.opened
    sidebar.value.withoutAnimation = false
  }

  const closeSidebar = (withoutAnimation = false) => {
    sidebar.value.opened = false
    sidebar.value.withoutAnimation = withoutAnimation
  }

  const openSidebar = (withoutAnimation = false) => {
    sidebar.value.opened = true
    sidebar.value.withoutAnimation = withoutAnimation
  }

  const toggleDevice = (deviceType) => {
    device.value = deviceType
  }

  const setSize = (newSize) => {
    size.value = newSize
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
    // 设置HTML属性用于CSS变量切换
    document.documentElement.setAttribute('data-theme', newTheme)
    // 保存到本地存储
    localStorage.setItem('theme', newTheme)
  }

  const setLanguage = (newLanguage) => {
    language.value = newLanguage
    localStorage.setItem('language', newLanguage)
  }

  const setLoading = (status) => {
    loading.value = status
  }

  const setUnreadNotifications = (count) => {
    unreadNotifications.value = count
  }

  // 初始化应用设置
  const initApp = () => {
    // 从本地存储恢复设置
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      setTheme(savedTheme)
    }

    const savedLanguage = localStorage.getItem('language')
    if (savedLanguage) {
      setLanguage(savedLanguage)
    }

    const savedSidebarStatus = localStorage.getItem('sidebarStatus')
    if (savedSidebarStatus) {
      sidebar.value.opened = savedSidebarStatus === 'opened'
    }

    // 检测设备类型
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    if (isMobile) {
      toggleDevice('mobile')
      closeSidebar(true)
    }

    // 监听窗口大小变化
    window.addEventListener('resize', () => {
      if (window.innerWidth < 992) {
        toggleDevice('mobile')
        closeSidebar(true)
      } else {
        toggleDevice('desktop')
      }
    })
  }

  // 保存侧边栏状态
  const saveSidebarStatus = () => {
    localStorage.setItem('sidebarStatus', sidebar.value.opened ? 'opened' : 'closed')
  }

  return {
    // 状态
    sidebar,
    device,
    size,
    theme,
    language,
    loading,
    unreadNotifications,
    
    // 方法
    toggleSidebar,
    closeSidebar,
    openSidebar,
    toggleDevice,
    setSize,
    setTheme,
    setLanguage,
    setLoading,
    setUnreadNotifications,
    initApp,
    saveSidebarStatus
  }
})
