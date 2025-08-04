import Cookies from 'js-cookie'

const TokenKey = 'todo_token'
const RefreshTokenKey = 'todo_refresh_token'

// Token相关操作
export function getToken() {
  return Cookies.get(TokenKey) || localStorage.getItem(TokenKey)
}

export function setToken(token) {
  Cookies.set(TokenKey, token, { expires: 7 }) // 7天过期
  localStorage.setItem(TokenKey, token)
}

export function removeToken() {
  Cookies.remove(TokenKey)
  localStorage.removeItem(TokenKey)
}

// Refresh Token相关操作
export function getRefreshToken() {
  return localStorage.getItem(RefreshTokenKey)
}

export function setRefreshToken(token) {
  localStorage.setItem(RefreshTokenKey, token)
}

export function removeRefreshToken() {
  localStorage.removeItem(RefreshTokenKey)
}

// 清除所有认证信息
export function clearAuth() {
  removeToken()
  removeRefreshToken()
  localStorage.removeItem('user_info')
  localStorage.removeItem('user_permissions')
}

// 检查token是否过期
export function isTokenExpired(token) {
  if (!token) return true
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Date.now() / 1000
    return payload.exp < currentTime
  } catch (error) {
    return true
  }
}

// 获取token中的用户信息
export function getTokenInfo(token) {
  if (!token) return null
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      userId: payload.user_id,
      username: payload.username,
      exp: payload.exp,
      iat: payload.iat
    }
  } catch (error) {
    return null
  }
}

// 格式化权限检查
export function hasPermission(userPermissions, permission) {
  if (!userPermissions || !permission) return false
  
  // 如果是管理员，拥有所有权限
  if (userPermissions.is_admin) return true
  
  // 检查具体权限
  return userPermissions[permission] === true
}

// 检查用户角色
export function hasRole(userInfo, role) {
  if (!userInfo || !role) return false
  return userInfo.role === role
}

// 检查是否可以访问路由
export function canAccessRoute(route, userInfo, userPermissions) {
  // 不需要认证的路由
  if (!route.meta?.requiresAuth) return true
  
  // 需要认证但用户未登录
  if (!userInfo) return false
  
  // 检查权限要求
  if (route.meta?.permission) {
    return hasPermission(userPermissions, route.meta.permission)
  }
  
  // 检查角色要求
  if (route.meta?.roles) {
    return route.meta.roles.some(role => hasRole(userInfo, role))
  }
  
  return true
}
