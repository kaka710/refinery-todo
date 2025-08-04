<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  // 应用启动时检查登录状态
  userStore.checkLoginStatus()
})
</script>

<style lang="scss">
#app {
  height: 100vh;
  width: 100vw;
}

// 全局样式重置
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// 滚动条样式
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

// Element Plus 样式覆盖
.el-message {
  min-width: 300px;
}

.el-notification {
  min-width: 350px;
}

// 自定义类
.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.text-left {
  text-align: left;
}

.flex {
  display: flex;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.flex-1 {
  flex: 1;
}

.mb-16 {
  margin-bottom: 16px;
}

.mb-24 {
  margin-bottom: 24px;
}

.mt-16 {
  margin-top: 16px;
}

.mt-24 {
  margin-top: 24px;
}

.ml-8 {
  margin-left: 8px;
}

.mr-8 {
  margin-right: 8px;
}

.p-16 {
  padding: 16px;
}

.p-24 {
  padding: 24px;
}

.cursor-pointer {
  cursor: pointer;
}

.full-width {
  width: 100%;
}

.full-height {
  height: 100%;
}
</style>
