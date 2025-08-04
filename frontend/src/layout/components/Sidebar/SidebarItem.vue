<template>
  <div v-if="!item.hidden">
    <!-- 有子菜单的情况 -->
    <el-sub-menu
      v-if="hasChildren"
      :index="resolvePath(item.path)"
      popper-append-to-body
    >
      <template #title>
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <span v-if="item.meta && item.meta.title">{{ item.meta.title }}</span>
      </template>
      
      <SidebarItem
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(child.path)"
      />
    </el-sub-menu>
    
    <!-- 没有子菜单的情况 -->
    <router-link
      v-else
      :to="resolvePath(item.path)"
      custom
      v-slot="{ navigate, isActive }"
    >
      <el-menu-item 
        :index="resolvePath(item.path)"
        :class="{ 'is-active': isActive }"
        @click="navigate"
      >
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <template #title>
          <span v-if="item.meta && item.meta.title">{{ item.meta.title }}</span>
        </template>
      </el-menu-item>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ElSubMenu, ElMenuItem, ElIcon } from 'element-plus'
import { isExternal } from '@/utils'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  basePath: {
    type: String,
    default: ''
  }
})

// 计算属性
const hasChildren = computed(() => {
  return props.item.children && 
         props.item.children.length > 0 && 
         props.item.children.some(child => !child.hidden)
})

// 方法
const resolvePath = (routePath) => {
  if (isExternal(routePath)) {
    return routePath
  }
  
  if (isExternal(props.basePath)) {
    return props.basePath
  }
  
  // 确保路径以 / 开头
  if (!routePath.startsWith('/')) {
    routePath = '/' + routePath
  }
  
  return routePath
}
</script>

<style lang="scss" scoped>
.el-menu-item,
.el-sub-menu {
  &:hover {
    background-color: var(--sidebar-hover-bg-color, #263445) !important;
  }
}

.el-menu-item.is-active {
  background-color: var(--sidebar-active-bg-color, #409eff) !important;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background-color: var(--sidebar-active-border-color, #409eff);
  }
}
</style>
