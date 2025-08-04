import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getToken } from './auth'
import router from '@/router'

// 强制HTTPS检查
const forceHTTPS = () => {
  if (import.meta.env.VITE_FORCE_HTTPS === 'true' && location.protocol === 'http:') {
    location.replace(location.href.replace('http:', 'https:'))
  }
}

// 执行HTTPS检查
forceHTTPS()

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加认证token
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加请求时间戳，防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果是文件下载，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 正常响应
    return response
  },
  async error => {
    console.error('响应错误:', error)
    
    const { response } = error
    
    if (!response) {
      ElMessage.error('网络连接异常，请检查网络设置')
      return Promise.reject(error)
    }
    
    const { status, data } = response
    
    switch (status) {
      case 400:
        // 请求参数错误
        if (data && data.detail) {
          ElMessage.error(data.detail)
        } else if (data && typeof data === 'object') {
          // 处理表单验证错误
          const errors = []
          Object.keys(data).forEach(key => {
            if (Array.isArray(data[key])) {
              errors.push(...data[key])
            } else {
              errors.push(data[key])
            }
          })
          ElMessage.error(errors.join('; '))
        } else {
          ElMessage.error('请求参数错误')
        }
        break
        
      case 401:
        // 未授权，token过期或无效
        ElMessage.error('登录已过期，请重新登录')
        const userStore = useUserStore()
        userStore.clearUserData()
        router.push('/login')
        break
        
      case 403:
        // 权限不足
        ElMessage.error('权限不足，无法访问该资源')
        router.push('/403')
        break
        
      case 404:
        // 资源不存在
        ElMessage.error('请求的资源不存在')
        break
        
      case 422:
        // 数据验证错误
        if (data && data.detail) {
          if (Array.isArray(data.detail)) {
            const errors = data.detail.map(item => item.msg || item.message || item).join('; ')
            ElMessage.error(errors)
          } else {
            ElMessage.error(data.detail)
          }
        } else {
          ElMessage.error('数据验证失败')
        }
        break
        
      case 429:
        // 请求过于频繁
        ElMessage.error('请求过于频繁，请稍后再试')
        break
        
      case 500:
        // 服务器内部错误
        ElMessage.error('服务器内部错误，请联系管理员')
        break
        
      case 502:
      case 503:
      case 504:
        // 服务器错误
        ElMessage.error('服务暂时不可用，请稍后再试')
        break
        
      default:
        ElMessage.error(data?.detail || data?.message || '请求失败')
    }
    
    return Promise.reject(error)
  }
)

// 请求方法封装
export const request = {
  get(url, params = {}, config = {}) {
    return service.get(url, { params, ...config })
  },
  
  post(url, data = {}, config = {}) {
    return service.post(url, data, config)
  },
  
  put(url, data = {}, config = {}) {
    return service.put(url, data, config)
  },
  
  patch(url, data = {}, config = {}) {
    return service.patch(url, data, config)
  },
  
  delete(url, config = {}) {
    return service.delete(url, config)
  },
  
  upload(url, formData, config = {}) {
    return service.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  },
  
  download(url, params = {}, filename = '') {
    return service.get(url, {
      params,
      responseType: 'blob'
    }).then(response => {
      // 创建下载链接
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      
      // 从响应头获取文件名
      const contentDisposition = response.headers['content-disposition']
      if (contentDisposition && !filename) {
        const matches = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (matches && matches[1]) {
          filename = matches[1].replace(/['"]/g, '')
        }
      }
      
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      
      return response
    })
  }
}

export default service
