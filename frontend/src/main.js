import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'
import './styles/index.scss'

// 导入浏览器优化工具
import {
  initBrowserOptimizations,
  initPerformanceMonitoring,
  initMemoryLeakDetection
} from './utils/browser'

// 导入HTTPS强制工具
import { initHTTPSCheck, showHTTPSInfo } from './utils/https'

// 初始化HTTPS检查（优先级最高）
initHTTPSCheck()
showHTTPSInfo()

// 初始化浏览器优化（只调用一次）
initBrowserOptimizations()

// 开发环境下启用性能监控
if (import.meta.env.DEV) {
  initPerformanceMonitoring()
  initMemoryLeakDetection()
}

// 创建应用实例
const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
  size: 'default'
})

// 挂载应用
app.mount('#app')
