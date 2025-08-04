<template>
  <div class="organization">
    <!-- 导航标签页 -->
    <div class="nav-tabs">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="org-tabs">
        <el-tab-pane label="部门管理" name="departments">
          <template #label>
            <span class="tab-label">
              <el-icon><OfficeBuilding /></el-icon>
              部门管理
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="全部人员" name="users">
          <template #label>
            <span class="tab-label">
              <el-icon><UserFilled /></el-icon>
              全部人员
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 子路由内容 -->
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { OfficeBuilding, UserFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const activeTab = ref('departments')

// 根据当前路由设置活动标签
const updateActiveTab = () => {
  if (route.name === 'AllUsers') {
    activeTab.value = 'users'
  } else {
    activeTab.value = 'departments'
  }
}

// 处理标签切换
const handleTabChange = (tabName) => {
  if (tabName === 'users') {
    router.push({ name: 'AllUsers' })
  } else {
    router.push({ name: 'DepartmentList' })
  }
}

// 监听路由变化
watch(() => route.name, updateActiveTab, { immediate: true })
</script>

<style scoped>
.organization {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.nav-tabs {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}

.org-tabs {
  margin-bottom: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.content-area {
  flex: 1;
  overflow: hidden;
}

:deep(.el-tabs__header) {
  margin: 0;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.el-tabs__item) {
  padding: 0 20px;
  height: 50px;
  line-height: 50px;
  font-weight: 500;
}

:deep(.el-tabs__item.is-active) {
  color: #409eff;
}
</style>
