import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置NProgress
NProgress.configure({ showSpinner: false })

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
      hideInMenu: true
    }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: {
          title: '工作台',
          icon: 'House',
          requiresAuth: true
        }
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/tasks/index.vue'),
        meta: {
          title: '任务管理',
          icon: 'List',
          requiresAuth: true
        },
        children: [
          {
            path: '',
            name: 'TaskList',
            component: () => import('@/views/tasks/TaskList.vue'),
            meta: {
              title: '任务列表',
              requiresAuth: true
            }
          },
          {
            path: 'create',
            name: 'TaskCreate',
            component: () => import('@/views/tasks/TaskCreate.vue'),
            meta: {
              title: '创建任务',
              requiresAuth: true,
              permission: 'can_create_task'
            }
          },
          {
            path: 'debug',
            name: 'TaskDebug',
            component: () => import('@/views/tasks/debug.vue'),
            meta: {
              title: '调试页面',
              requiresAuth: true
            }
          },
          {
            path: 'test',
            name: 'TaskTest',
            component: () => import('@/views/tasks/简单测试.vue'),
            meta: {
              title: '简单测试',
              requiresAuth: true
            }
          },
          {
            path: 'min-test',
            name: 'MinTest',
            component: () => import('@/views/tasks/最小测试.vue'),
            meta: {
              title: '最小测试',
              requiresAuth: true
            }
          },
          {
            path: ':id',
            name: 'TaskDetail',
            component: () => import('@/views/tasks/TaskDetail.vue'),
            meta: {
              title: '任务详情',
              requiresAuth: true,
              hideInMenu: true
            }
          },
          {
            path: ':id/edit',
            name: 'TaskEdit',
            component: () => import('@/views/tasks/TaskEdit.vue'),
            meta: {
              title: '编辑任务',
              requiresAuth: true,
              hideInMenu: true
            }
          }
        ]
      },
      {
        path: 'my-tasks',
        name: 'MyTasks',
        component: () => import('@/views/tasks/MyTasks.vue'),
        meta: {
          title: '我的任务',
          icon: 'User',
          requiresAuth: true
        }
      },
      {
        path: 'departments',
        name: 'Departments',
        component: () => import('@/views/departments/index.vue'),
        meta: {
          title: '组织架构',
          icon: 'OfficeBuilding',
          requiresAuth: true,
          permission: 'is_admin'
        },
        children: [
          {
            path: '',
            name: 'DepartmentList',
            component: () => import('@/views/departments/DepartmentList.vue'),
            meta: {
              title: '部门管理',
              requiresAuth: true,
              permission: 'is_admin'
            }
          },
          {
            path: ':id/users',
            name: 'DepartmentUsers',
            component: () => import('@/views/departments/DepartmentUsers.vue'),
            meta: {
              title: '部门人员',
              requiresAuth: true,
              permission: 'is_admin',
              hideInMenu: true
            }
          },
          {
            path: 'users',
            name: 'AllUsers',
            component: () => import('@/views/departments/AllUsers.vue'),
            meta: {
              title: '全部人员',
              requiresAuth: true,
              permission: 'is_admin'
            }
          }
        ]
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('@/views/notifications/index.vue'),
        meta: {
          title: '通知中心',
          icon: 'Bell',
          requiresAuth: true
        }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/reports/index.vue'),
        meta: {
          title: '统计报表',
          icon: 'DataAnalysis',
          requiresAuth: true
        }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: {
          title: '系统设置',
          icon: 'Setting',
          requiresAuth: true
        },
        children: [
          {
            path: 'profile',
            name: 'Profile',
            component: () => import('@/views/settings/Profile.vue'),
            meta: {
              title: '个人资料',
              requiresAuth: true
            }
          },
          {
            path: 'notifications',
            name: 'NotificationSettings',
            component: () => import('@/views/settings/NotificationSettings.vue'),
            meta: {
              title: '通知设置',
              requiresAuth: true
            }
          },
          {
            path: 'integrations',
            name: 'Integrations',
            component: () => import('@/views/settings/Integrations.vue'),
            meta: {
              title: '集成设置',
              requiresAuth: true,
              permission: 'is_admin'
            }
          }
        ]
      }
    ]
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/error/403.vue'),
    meta: {
      title: '权限不足',
      hideInMenu: true
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面不存在',
      hideInMenu: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start()

  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 海南炼化Todo系统`
  }

  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      // 尝试从本地存储恢复登录状态
      await userStore.checkLoginStatus()

      if (!userStore.isLoggedIn) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      }
    }

    // 检查权限
    if (to.meta.permission) {
      const hasPermission = userStore.hasPermission(to.meta.permission)
      if (!hasPermission) {
        next('/403')
        return
      }
    }
  }

  // 如果已登录用户访问登录页，重定向到首页
  if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
    return
  }

  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
