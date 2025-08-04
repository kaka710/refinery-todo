<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item v-for="(item, index) in levelList" :key="item.path">
        <span
          v-if="item.redirect === 'noRedirect' || index === levelList.length - 1"
          class="no-redirect"
        >
          {{ item.meta.title }}
        </span>
        <a v-else @click.prevent="handleLink(item)">
          {{ item.meta.title }}
        </a>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const levelList = ref([])

const getBreadcrumb = () => {
  // 过滤掉没有meta.title的路由
  let matched = route.matched.filter(item => item.meta && item.meta.title)
  
  const first = matched[0]
  
  // 如果第一个不是dashboard，添加dashboard
  if (!isDashboard(first)) {
    matched = [{ path: '/dashboard', meta: { title: '工作台' } }].concat(matched)
  }
  
  levelList.value = matched.filter(item => {
    return item.meta && item.meta.title && item.meta.breadcrumb !== false
  })
}

const isDashboard = (route) => {
  const name = route && route.name
  if (!name) {
    return false
  }
  return name.trim().toLocaleLowerCase() === 'Dashboard'.toLocaleLowerCase()
}

const pathCompile = (path) => {
  const { params } = route
  const toPath = path
  return toPath.replace(/:(\w+)/g, (match, key) => {
    return params[key] || match
  })
}

const handleLink = (item) => {
  const { redirect, path } = item
  if (redirect) {
    router.push(redirect)
    return
  }
  router.push(pathCompile(path))
}

// 监听路由变化
watch(route, getBreadcrumb, { immediate: true })
</script>

<style lang="scss" scoped>
.app-breadcrumb.el-breadcrumb {
  display: inline-block;
  font-size: 14px;
  line-height: 50px;
  margin-left: 8px;

  .no-redirect {
    color: var(--text-color-placeholder);
    cursor: text;
  }
}

.breadcrumb-enter-active,
.breadcrumb-leave-active {
  transition: all 0.5s;
}

.breadcrumb-enter-from,
.breadcrumb-leave-active {
  opacity: 0;
  transform: translateX(20px);
}

.breadcrumb-move {
  transition: all 0.5s;
}

.breadcrumb-leave-active {
  position: absolute;
}
</style>
