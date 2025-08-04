import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'
import duration from 'dayjs/plugin/duration'

// 配置dayjs
dayjs.locale('zh-cn')
dayjs.extend(relativeTime)
dayjs.extend(duration)

/**
 * 格式化日期时间
 * @param {string|Date} date 日期
 * @param {string} format 格式
 * @returns {string}
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''
  return dayjs(date).format(format)
}

/**
 * 格式化相对时间
 * @param {string|Date} date 日期
 * @returns {string}
 */
export function formatRelativeTime(date) {
  if (!date) return ''
  return dayjs(date).fromNow()
}

/**
 * 格式化文件大小
 * @param {number} bytes 字节数
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 防抖函数
 * @param {Function} func 要防抖的函数
 * @param {number} wait 等待时间
 * @param {boolean} immediate 是否立即执行
 * @returns {Function}
 */
export function debounce(func, wait, immediate) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      timeout = null
      if (!immediate) func(...args)
    }
    const callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func(...args)
  }
}

/**
 * 节流函数
 * @param {Function} func 要节流的函数
 * @param {number} limit 时间间隔
 * @returns {Function}
 */
export function throttle(func, limit) {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * 深拷贝
 * @param {any} obj 要拷贝的对象
 * @returns {any}
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime())
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (typeof obj === 'object') {
    const clonedObj = {}
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
}

/**
 * 生成随机字符串
 * @param {number} length 长度
 * @returns {string}
 */
export function generateRandomString(length = 8) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 获取文件扩展名
 * @param {string} filename 文件名
 * @returns {string}
 */
export function getFileExtension(filename) {
  if (!filename) return ''
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2)
}

/**
 * 检查是否为图片文件
 * @param {string} filename 文件名
 * @returns {boolean}
 */
export function isImageFile(filename) {
  const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
  const ext = getFileExtension(filename).toLowerCase()
  return imageExtensions.includes(ext)
}

/**
 * 检查是否为文档文件
 * @param {string} filename 文件名
 * @returns {boolean}
 */
export function isDocumentFile(filename) {
  const docExtensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt']
  const ext = getFileExtension(filename).toLowerCase()
  return docExtensions.includes(ext)
}

/**
 * 获取任务状态显示信息
 * @param {string} status 状态值
 * @returns {object}
 */
export function getTaskStatusInfo(status) {
  const statusMap = {
    draft: { text: '草稿', type: 'info', color: '#909399' },
    pending: { text: '待接收', type: 'warning', color: '#e6a23c' },
    accepted: { text: '已接收', type: 'primary', color: '#409eff' },
    in_progress: { text: '进行中', type: 'primary', color: '#409eff' },
    completed: { text: '已完成', type: 'success', color: '#67c23a' },
    reviewed: { text: '已评价', type: 'success', color: '#67c23a' },
    cancelled: { text: '已取消', type: 'info', color: '#909399' },
    overdue: { text: '已逾期', type: 'danger', color: '#f56c6c' }
  }
  return statusMap[status] || { text: status, type: 'info', color: '#909399' }
}

/**
 * 获取优先级显示信息
 * @param {string} priority 优先级值
 * @returns {object}
 */
export function getPriorityInfo(priority) {
  const priorityMap = {
    low: { text: '低', type: 'info', color: '#909399' },
    medium: { text: '中', type: 'warning', color: '#e6a23c' },
    high: { text: '高', type: 'danger', color: '#f56c6c' },
    critical: { text: '紧急', type: 'danger', color: '#ff4d4f' }
  }
  return priorityMap[priority] || { text: priority, type: 'info', color: '#909399' }
}

/**
 * 获取用户角色显示信息
 * @param {string} role 角色值
 * @returns {object}
 */
export function getRoleInfo(role) {
  const roleMap = {
    admin: { text: '系统管理员', type: 'danger', color: '#f56c6c' },
    dept_manager: { text: '部门负责人', type: 'warning', color: '#e6a23c' },
    prof_manager: { text: '专业负责人', type: 'primary', color: '#409eff' },
    executor: { text: '执行人', type: 'success', color: '#67c23a' }
  }
  return roleMap[role] || { text: role, type: 'info', color: '#909399' }
}

/**
 * 计算任务进度百分比
 * @param {object} task 任务对象
 * @returns {number}
 */
export function calculateTaskProgress(task) {
  if (!task || !task.assignments) return 0
  
  const assignments = task.assignments
  if (assignments.length === 0) return 0
  
  const completedCount = assignments.filter(assignment => 
    assignment.status === 'completed'
  ).length
  
  return Math.round((completedCount / assignments.length) * 100)
}

/**
 * 检查任务是否逾期
 * @param {object} task 任务对象
 * @returns {boolean}
 */
export function isTaskOverdue(task) {
  if (!task || !task.due_date) return false
  
  const now = dayjs()
  const dueDate = dayjs(task.due_date)
  
  return now.isAfter(dueDate) && !['completed', 'reviewed', 'cancelled'].includes(task.status)
}

/**
 * 获取任务剩余时间
 * @param {object} task 任务对象
 * @returns {string}
 */
export function getTaskRemainingTime(task) {
  if (!task || !task.due_date) return ''
  
  const now = dayjs()
  const dueDate = dayjs(task.due_date)
  
  if (now.isAfter(dueDate)) {
    return `逾期 ${now.to(dueDate)}`
  } else {
    return `剩余 ${dueDate.fromNow()}`
  }
}

/**
 * 验证邮箱格式
 * @param {string} email 邮箱地址
 * @returns {boolean}
 */
export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

/**
 * 验证手机号格式
 * @param {string} phone 手机号
 * @returns {boolean}
 */
export function validatePhone(phone) {
  const re = /^1[3-9]\d{9}$/
  return re.test(phone)
}

/**
 * 检查是否为外部链接
 * @param {string} path 路径
 * @returns {boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * 下载文件
 * @param {string} url 文件URL
 * @param {string} filename 文件名
 */
export function downloadFile(url, filename) {
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
