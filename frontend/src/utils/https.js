/**
 * HTTPS强制重定向工具
 * 确保应用只能通过HTTPS访问
 */

/**
 * 检查并强制重定向到HTTPS
 */
export function forceHTTPS() {
  // 检查环境变量是否启用HTTPS强制
  const forceHTTPS = import.meta.env.VITE_FORCE_HTTPS === 'true'
  const httpsOnly = import.meta.env.VITE_HTTPS_ONLY === 'true'
  
  if ((forceHTTPS || httpsOnly) && location.protocol === 'http:') {
    // 构建HTTPS URL
    const httpsUrl = location.href.replace('http:', 'https:')
    
    // 显示重定向提示
    console.warn('🔒 强制重定向到HTTPS:', httpsUrl)
    
    // 重定向到HTTPS
    location.replace(httpsUrl)
    return true
  }
  
  return false
}

/**
 * 验证当前连接是否为HTTPS
 */
export function isHTTPS() {
  return location.protocol === 'https:'
}

/**
 * 获取HTTPS版本的URL
 */
export function getHTTPSUrl(url) {
  if (typeof url === 'string') {
    return url.replace(/^http:/, 'https:')
  }
  return url
}

/**
 * 确保API请求使用HTTPS
 */
export function ensureHTTPSApiUrl(baseURL) {
  if (!baseURL) return baseURL
  
  // 如果是相对路径，使用当前协议
  if (baseURL.startsWith('/')) {
    return baseURL
  }
  
  // 如果是绝对路径，确保使用HTTPS
  return getHTTPSUrl(baseURL)
}

/**
 * 初始化HTTPS检查
 * 在应用启动时调用
 */
export function initHTTPSCheck() {
  // 立即检查并重定向
  if (forceHTTPS()) {
    return
  }
  
  // 监听页面可见性变化，确保用户回到页面时仍然是HTTPS
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      forceHTTPS()
    }
  })
  
  // 监听popstate事件，防止用户通过浏览器历史回到HTTP
  window.addEventListener('popstate', () => {
    setTimeout(() => {
      forceHTTPS()
    }, 100)
  })
  
  console.log('🔒 HTTPS检查已初始化')
}

/**
 * 显示HTTPS安全提示
 */
export function showHTTPSInfo() {
  if (isHTTPS()) {
    console.log('🔒 当前连接已使用HTTPS加密')
  } else {
    console.warn('⚠️ 当前连接未使用HTTPS加密')
  }
}
