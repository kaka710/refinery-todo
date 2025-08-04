<template>
  <div style="padding: 20px; max-width: 800px;">
    <h1>🔍 部门数据测试页面</h1>
    
    <!-- 基础信息 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>📊 数据状态</span>
      </template>
      <p><strong>departments 数组长度:</strong> {{ departments.length }}</p>
      <p><strong>是否为数组:</strong> {{ Array.isArray(departments) }}</p>
      <p><strong>数据类型:</strong> {{ typeof departments }}</p>
    </el-card>

    <!-- 原始数据 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>📋 原始模拟数据</span>
      </template>
      <div style="background: #f5f5f5; padding: 10px; border-radius: 4px;">
        <pre>{{ JSON.stringify(mockDepartments, null, 2) }}</pre>
      </div>
    </el-card>

    <!-- 当前数据 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>💾 当前 departments 数据</span>
      </template>
      <div style="background: #f5f5f5; padding: 10px; border-radius: 4px;">
        <pre>{{ JSON.stringify(departments, null, 2) }}</pre>
      </div>
    </el-card>

    <!-- 选择器测试 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>🎯 选择器测试</span>
      </template>
      
      <div style="margin-bottom: 20px;">
        <h4>方法1: 直接使用 mockDepartments</h4>
        <el-select v-model="test1" placeholder="选择部门" style="width: 300px;">
          <el-option
            v-for="dept in mockDepartments"
            :key="dept.id"
            :label="dept.name"
            :value="dept.id"
          >
            {{ dept.name }} ({{ dept.code }})
          </el-option>
        </el-select>
        <span style="margin-left: 10px;">选中: {{ test1 }}</span>
      </div>

      <div style="margin-bottom: 20px;">
        <h4>方法2: 使用 departments 响应式数据</h4>
        <el-select v-model="test2" placeholder="选择部门" style="width: 300px;">
          <el-option
            v-for="dept in departments"
            :key="dept.id"
            :label="dept.name"
            :value="dept.id"
          >
            {{ dept.name }} ({{ dept.code }})
          </el-option>
        </el-select>
        <span style="margin-left: 10px;">选中: {{ test2 }}</span>
      </div>

      <div>
        <h4>方法3: 手动循环显示</h4>
        <div v-for="dept in departments" :key="dept.id" style="padding: 5px; border: 1px solid #ddd; margin: 2px;">
          ID: {{ dept.id }}, 名称: {{ dept.name }}, 代码: {{ dept.code }}
        </div>
      </div>
    </el-card>

    <!-- 操作按钮 -->
    <el-card>
      <template #header>
        <span>🔧 操作</span>
      </template>
      <el-button @click="loadDepartments" type="primary">重新加载部门数据</el-button>
      <el-button @click="clearDepartments" type="danger">清空数据</el-button>
      <el-button @click="testData" type="success">测试数据</el-button>
    </el-card>

    <!-- 日志 -->
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>📝 操作日志</span>
      </template>
      <div style="background: #000; color: #0f0; padding: 10px; border-radius: 4px; font-family: monospace; max-height: 200px; overflow-y: auto;">
        <div v-for="(log, index) in logs" :key="index">{{ log }}</div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const departments = ref([])
const test1 = ref('')
const test2 = ref('')
const logs = ref([])

// 模拟部门数据
const mockDepartments = [
  { id: 1, name: '生产部', code: 'PROD', description: '负责生产运营' },
  { id: 2, name: '技术部', code: 'TECH', description: '负责技术研发' },
  { id: 3, name: '质量部', code: 'QC', description: '负责质量管控' },
  { id: 4, name: '安全部', code: 'SAFE', description: '负责安全管理' },
  { id: 5, name: '设备部', code: 'EQUIP', description: '负责设备维护' }
]

// 添加日志
const addLog = (message) => {
  const timestamp = new Date().toLocaleTimeString()
  logs.value.push(`[${timestamp}] ${message}`)
  console.log(message)
}

// 加载部门列表
const loadDepartments = async () => {
  try {
    addLog('开始加载部门数据...')
    addLog(`mockDepartments 长度: ${mockDepartments.length}`)
    
    departments.value = mockDepartments
    
    addLog(`departments.value 赋值后长度: ${departments.value.length}`)
    addLog(`departments.value 内容: ${JSON.stringify(departments.value)}`)
    
    ElMessage.success('部门数据加载成功')
  } catch (error) {
    addLog(`加载失败: ${error.message}`)
    ElMessage.error('加载部门列表失败')
  }
}

// 清空数据
const clearDepartments = () => {
  departments.value = []
  addLog('已清空 departments 数据')
}

// 测试数据
const testData = () => {
  addLog('=== 数据测试 ===')
  addLog(`mockDepartments 类型: ${typeof mockDepartments}`)
  addLog(`mockDepartments 是否为数组: ${Array.isArray(mockDepartments)}`)
  addLog(`departments.value 类型: ${typeof departments.value}`)
  addLog(`departments.value 是否为数组: ${Array.isArray(departments.value)}`)
  addLog(`departments.value 长度: ${departments.value.length}`)
  
  if (departments.value.length > 0) {
    addLog(`第一个元素: ${JSON.stringify(departments.value[0])}`)
  }
}

// 组件挂载时加载部门列表
onMounted(() => {
  addLog('组件已挂载')
  loadDepartments()
})
</script>

<style scoped>
pre {
  font-size: 12px;
  max-height: 150px;
  overflow-y: auto;
  margin: 0;
}

h4 {
  margin: 10px 0 5px 0;
  color: #409eff;
}
</style>
