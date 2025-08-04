<template>
  <div class="tasks-container">
    <el-card class="page-header">
      <div class="header-content">
        <h2>任务管理</h2>
        <p>管理和跟踪所有任务</p>
      </div>
    </el-card>
    
    <div class="tasks-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
// 任务管理主页面
</script>

<style scoped>
.tasks-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.header-content p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.tasks-content {
  min-height: 400px;
}
</style>
