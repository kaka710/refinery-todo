/**
 * 浏览器兼容性和警告处理工具
 */

/**
 * 禁用已弃用的 DOM Mutation Events 警告
 * 这些警告主要来自第三方库（如 Django Admin 的 Select2）
 */
export function suppressDeprecatedWarnings() {
  // 1. 重写console方法过滤警告
  const originalWarn = console.warn
  const originalLog = console.log
  const originalError = console.error

  // 过滤函数
  function shouldSuppressMessage(message) {
    const deprecatedWarnings = [
      'DOMNodeInsertedIntoDocument',
      'DOMNodeInserted',
      'DOMNodeRemoved',
      'DOMAttrModified',
      'DOMCharacterDataModified',
      'DOMSubtreeModified',
      'DOM Mutation Event',
      'deprecated',
      'legacy-event-types',
      'Deprecation',
      'synchronous'
    ]

    return deprecatedWarnings.some(warning =>
      message.toLowerCase().includes(warning.toLowerCase())
    )
  }

  // 重写console.warn（安全版本）
  console.warn = function(...args) {
    try {
      // 安全地转换参数为字符串
      const message = args.map(arg => {
        if (arg === null) return 'null'
        if (arg === undefined) return 'undefined'
        if (typeof arg === 'object') {
          try {
            return JSON.stringify(arg)
          } catch (e) {
            return '[Object]'
          }
        }
        return String(arg)
      }).join(' ')

      if (!shouldSuppressMessage(message)) {
        originalWarn.apply(console, args)
      }
    } catch (e) {
      // 如果处理失败，直接调用原始方法
      originalWarn.apply(console, args)
    }
  }

  // 重写console.log（某些警告可能通过log输出）- 安全版本
  console.log = function(...args) {
    try {
      // 安全地转换参数为字符串
      const message = args.map(arg => {
        if (arg === null) return 'null'
        if (arg === undefined) return 'undefined'
        if (typeof arg === 'object') {
          try {
            return JSON.stringify(arg)
          } catch (e) {
            return '[Object]'
          }
        }
        return String(arg)
      }).join(' ')

      if (!shouldSuppressMessage(message)) {
        originalLog.apply(console, args)
      }
    } catch (e) {
      // 如果处理失败，直接调用原始方法
      originalLog.apply(console, args)
    }
  }

  // 2. 尝试阻止DOM事件监听器的添加（实验性）
  try {
    const originalAddEventListener = EventTarget.prototype.addEventListener
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      // 如果是已弃用的DOM事件，静默忽略或替换为MutationObserver
      const deprecatedEvents = [
        'DOMNodeInsertedIntoDocument',
        'DOMNodeInserted',
        'DOMNodeRemoved',
        'DOMAttrModified',
        'DOMCharacterDataModified',
        'DOMSubtreeModified'
      ]

      if (deprecatedEvents.includes(type)) {
        // 静默忽略弃用的DOM事件监听器
        console.debug(`🔇 已阻止添加弃用的DOM事件监听器: ${type}`)
        return
      }

      // 正常事件继续处理
      return originalAddEventListener.call(this, type, listener, options)
    }
  } catch (e) {
    console.debug('无法重写addEventListener:', e)
  }

  console.log('🔇 已启用增强型弃用警告过滤')
}

/**
 * 确保资源使用正确的协议
 * 避免 Mixed Content 警告
 */
export function ensureSecureProtocol() {
  // 如果当前页面是 HTTPS，确保所有资源也使用 HTTPS
  if (location.protocol === 'https:') {
    // 检查并修复可能的 HTTP 资源引用
    const images = document.querySelectorAll('img[src^="http:"]')
    const links = document.querySelectorAll('link[href^="http:"]')
    const scripts = document.querySelectorAll('script[src^="http:"]')
    
    // 将 HTTP 资源升级为 HTTPS
    ;[...images, ...links, ...scripts].forEach(element => {
      const attr = element.src ? 'src' : 'href'
      if (element[attr] && element[attr].startsWith('http:')) {
        element[attr] = element[attr].replace('http:', 'https:')
      }
    })
  }
}

/**
 * 检查浏览器兼容性
 */
export function checkBrowserCompatibility() {
  const features = {
    mutationObserver: 'MutationObserver' in window,
    intersectionObserver: 'IntersectionObserver' in window,
    fetch: 'fetch' in window,
    promise: 'Promise' in window,
    es6: (() => {
      try {
        return eval('(function*(){})().next')
      } catch (e) {
        return false
      }
    })()
  }
  
  const unsupportedFeatures = Object.keys(features).filter(key => !features[key])
  
  if (unsupportedFeatures.length > 0) {
    console.warn('浏览器兼容性警告：以下功能不受支持：', unsupportedFeatures)
    return false
  }
  
  return true
}

/**
 * 初始化浏览器优化
 */
export function initBrowserOptimizations() {
  // 默认启用弃用警告过滤（开发环境）
  if (import.meta.env.DEV || import.meta.env.VITE_DISABLE_DEPRECATED_WARNINGS === 'true') {
    suppressDeprecatedWarnings()
    console.log('🔇 已启用弃用警告过滤')
  }
  
  // 确保安全协议
  ensureSecureProtocol()
  
  // 检查浏览器兼容性
  checkBrowserCompatibility()
  
  // 添加全局错误处理
  window.addEventListener('error', (event) => {
    // 过滤掉已知的无害错误
    const harmlessErrors = [
      'ResizeObserver loop limit exceeded',
      'Non-passive event listener',
      'Script error'
    ]
    
    const shouldIgnore = harmlessErrors.some(error => 
      event.message && event.message.includes(error)
    )
    
    if (!shouldIgnore) {
      console.error('全局错误捕获:', event.error)
    }
  })
  
  // 添加未处理的 Promise 拒绝处理
  window.addEventListener('unhandledrejection', (event) => {
    console.error('未处理的 Promise 拒绝:', event.reason)
    // 可以选择阻止默认的错误处理
    // event.preventDefault()
  })
}

/**
 * 性能监控
 */
export function initPerformanceMonitoring() {
  if ('performance' in window && 'PerformanceObserver' in window) {
    // 监控长任务（降低敏感度）
    try {
      let longTaskCount = 0
      const maxLongTaskWarnings = 3 // 最多显示3次警告

      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 100 && longTaskCount < maxLongTaskWarnings) { // 提高阈值到100ms
            longTaskCount++
            console.warn(`检测到长任务 (${longTaskCount}/${maxLongTaskWarnings}):`, {
              name: entry.name,
              duration: `${entry.duration.toFixed(2)}ms`,
              startTime: `${entry.startTime.toFixed(2)}ms`
            })

            if (longTaskCount >= maxLongTaskWarnings) {
              console.log('🔇 长任务警告已达到上限，后续警告将被抑制')
            }
          }
        }
      })

      observer.observe({ entryTypes: ['longtask'] })
    } catch (e) {
      // 某些浏览器可能不支持 longtask
      console.log('长任务监控不可用')
    }
  }
}

/**
 * 内存泄漏检测（开发环境）
 */
export function initMemoryLeakDetection() {
  if (import.meta.env.DEV && 'performance' in window && 'memory' in performance) {
    let lastMemoryUsage = performance.memory.usedJSHeapSize
    
    setInterval(() => {
      const currentMemoryUsage = performance.memory.usedJSHeapSize
      const memoryIncrease = currentMemoryUsage - lastMemoryUsage
      
      // 如果内存增长超过 10MB，发出警告
      if (memoryIncrease > 10 * 1024 * 1024) {
        console.warn('内存使用量显著增加:', {
          increase: `${(memoryIncrease / 1024 / 1024).toFixed(2)}MB`,
          current: `${(currentMemoryUsage / 1024 / 1024).toFixed(2)}MB`,
          limit: `${(performance.memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)}MB`
        })
      }
      
      lastMemoryUsage = currentMemoryUsage
    }, 30000) // 每30秒检查一次
  }
}
