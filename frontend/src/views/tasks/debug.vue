<template>
  <div style="padding: 20px;">
    <h2>调试页面 - 部门数据测试</h2>
    
    <el-card style="margin-bottom: 20px;">
      <h3>部门数据状态</h3>
      <p><strong>departments 数组长度:</strong> {{ departments.length }}</p>
      <p><strong>departments 内容:</strong></p>
      <pre>{{ JSON.stringify(departments, null, 2) }}</pre>
    </el-card>

    <el-card style="margin-bottom: 20px;">
      <h3>模拟数据</h3>
      <p><strong>mockDepartments 内容:</strong></p>
      <pre>{{ JSON.stringify(mockDepartments, null, 2) }}</pre>
    </el-card>

    <el-card>
      <h3>部门选择器测试</h3>
      <el-select v-model="selectedDept" placeholder="请选择部门" style="width: 300px;">
        <el-option
          v-for="dept in departments"
          :key="dept.id"
          :label="dept.name"
          :value="dept.id"
        >
          {{ dept.name }} ({{ dept.code }})
        </el-option>
      </el-select>
      <p style="margin-top: 10px;"><strong>选中的部门ID:</strong> {{ selectedDept }}</p>
    </el-card>

    <el-button @click="loadDepartments" type="primary" style="margin-top: 20px;">
      重新加载部门数据
    </el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const departments = ref([])
const selectedDept = ref('')

// 模拟部门数据
const mockDepartments = [
  { id: 1, name: '生产部', code: 'PROD', description: '负责生产运营' },
  { id: 2, name: '技术部', code: 'TECH', description: '负责技术研发' },
  { id: 3, name: '质量部', code: 'QC', description: '负责质量管控' },
  { id: 4, name: '安全部', code: 'SAFE', description: '负责安全管理' },
  { id: 5, name: '设备部', code: 'EQUIP', description: '负责设备维护' }
]

// 加载部门列表
const loadDepartments = async () => {
  try {
    console.log('开始加载部门数据...')
    departments.value = mockDepartments
    console.log('部门数据加载完成:', departments.value)
    ElMessage.success('部门数据加载成功')
  } catch (error) {
    console.error('加载部门列表失败:', error)
    ElMessage.error('加载部门列表失败')
  }
}

// 组件挂载时加载部门列表
onMounted(() => {
  console.log('组件挂载，开始加载部门数据')
  loadDepartments()
})
</script>

<style scoped>
pre {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}
</style>
