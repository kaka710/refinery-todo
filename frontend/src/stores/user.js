import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { login, logout, getUserInfo, refreshToken, getUserPermissions } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(getToken())
  const userInfo = ref(null)
  const permissions = ref({})
  const managedDepartments = ref([])

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value)
  
  const isAdmin = computed(() =>
    userInfo.value?.role === 'admin' ||
    userInfo.value?.is_superuser === true ||
    permissions.value?.is_admin === true
  )
  
  const isDeptManager = computed(() => userInfo.value?.role === 'dept_manager')
  
  const isProfManager = computed(() => userInfo.value?.role === 'prof_manager')
  
  const isExecutor = computed(() => userInfo.value?.role === 'executor')
  
  const canCreateTask = computed(() => {
    return permissions.value.can_create_task || false
  })
  
  const canManageUsers = computed(() => {
    return permissions.value.can_manage_users || false
  })

  // 方法
  const setUserToken = (newToken) => {
    token.value = newToken
    setToken(newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
  }

  const setPermissions = (perms) => {
    permissions.value = perms
    managedDepartments.value = perms.managed_departments || []
  }

  const clearUserData = () => {
    token.value = null
    userInfo.value = null
    permissions.value = {}
    managedDepartments.value = []
    removeToken()
  }

  // 登录
  const loginUser = async (loginForm) => {
    try {
      const response = await login(loginForm)
      const { access, refresh, user } = response.data

      // 保存token和用户信息
      setUserToken(access)
      setUserInfo(user)

      // 保存refresh token到localStorage
      localStorage.setItem('refresh_token', refresh)

      // 异步获取用户权限，不阻塞登录流程
      fetchUserPermissions().catch(error => {
        console.warn('获取用户权限失败，使用默认权限:', error)
      })

      ElMessage.success('登录成功')
      return response
    } catch (error) {
      // 错误消息已经在request拦截器中处理了，这里不需要重复显示
      console.error('登录失败:', error)
      throw error
    }
  }

  // 登出
  const logoutUser = async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refresh_token')
      if (refreshTokenValue) {
        await logout({ refresh: refreshTokenValue })
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      clearUserData()
      localStorage.removeItem('refresh_token')
      ElMessage.success('已退出登录')
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await getUserInfo()
      setUserInfo(response.data)
      return response.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  // 获取用户权限
  const fetchUserPermissions = async () => {
    try {
      // 添加超时控制，避免长时间等待
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('权限获取超时')), 3000) // 减少超时时间
      })

      // 尝试调用权限API，如果失败则使用默认权限
      try {
        const permissionsPromise = getUserPermissions()
        const response = await Promise.race([permissionsPromise, timeoutPromise])

        if (response && response.data) {
          setPermissions(response.data)
          console.log('权限获取成功')
        } else {
          throw new Error('权限数据格式错误')
        }
      } catch (apiError) {
        console.warn('权限API调用失败，使用默认权限:', apiError.message)
        setBasicPermissions()
      }
    } catch (error) {
      console.warn('获取用户权限失败，使用默认权限:', error.message)
      setBasicPermissions()
    }
  }

  // 设置基础权限的辅助函数
  const setBasicPermissions = () => {
    const basicPermissions = {
      can_create_task: true,
      can_manage_users: false,
      managed_departments: []
    }
    setPermissions(basicPermissions)
  }

  // 检查登录状态
  const checkLoginStatus = async () => {
    const savedToken = getToken()
    if (!savedToken) {
      return false
    }

    try {
      // 如果有token但没有用户信息，尝试获取
      if (!userInfo.value) {
        await fetchUserInfo()
        // 异步获取权限，不阻塞登录状态检查
        fetchUserPermissions().catch(error => {
          console.warn('权限获取失败:', error)
        })
      }
      return true
    } catch (error) {
      // token可能已过期，尝试刷新
      const refreshTokenValue = localStorage.getItem('refresh_token')
      if (refreshTokenValue) {
        try {
          const response = await refreshToken({ refresh: refreshTokenValue })
          setUserToken(response.data.access)
          await fetchUserInfo()
          // 异步获取权限，不阻塞token刷新
          fetchUserPermissions().catch(error => {
            console.warn('权限获取失败:', error)
          })
          return true
        } catch (refreshError) {
          console.error('刷新token失败:', refreshError)
          clearUserData()
          localStorage.removeItem('refresh_token')
          return false
        }
      } else {
        clearUserData()
        return false
      }
    }
  }

  // 检查权限
  const hasPermission = (permission) => {
    if (isAdmin.value) {
      return true // 管理员拥有所有权限
    }

    switch (permission) {
      case 'can_create_task':
        return canCreateTask.value
      case 'can_manage_users':
        return canManageUsers.value
      case 'is_admin':
        return isAdmin.value
      case 'is_dept_manager':
        return isDeptManager.value
      case 'is_prof_manager':
        return isProfManager.value
      default:
        return false
    }
  }

  // 检查是否可以访问部门
  const canAccessDepartment = (departmentId) => {
    if (isAdmin.value) {
      return true
    }
    
    if (isDeptManager.value) {
      return managedDepartments.value.some(dept => dept.id === departmentId)
    }
    
    return userInfo.value?.department?.id === departmentId
  }

  // 更新用户资料
  const updateProfile = async (profileData) => {
    try {
      // 这里应该调用更新资料的API
      // const response = await updateUserProfile(profileData)
      // setUserInfo({ ...userInfo.value, ...response.data })
      
      // 临时更新本地数据
      setUserInfo({ ...userInfo.value, ...profileData })
      ElMessage.success('资料更新成功')
    } catch (error) {
      ElMessage.error('资料更新失败')
      throw error
    }
  }

  return {
    // 状态
    token,
    userInfo,
    permissions,
    managedDepartments,
    
    // 计算属性
    isLoggedIn,
    isAdmin,
    isDeptManager,
    isProfManager,
    isExecutor,
    canCreateTask,
    canManageUsers,
    
    // 方法
    loginUser,
    logoutUser,
    fetchUserInfo,
    fetchUserPermissions,
    checkLoginStatus,
    hasPermission,
    canAccessDepartment,
    updateProfile,
    clearUserData
  }
})
