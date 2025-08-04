<template>
  <div style="padding: 20px;">
    <h1>最小测试页面</h1>
    
    <div style="margin: 20px 0;">
      <h3>测试1: 直接硬编码数据</h3>
      <el-select v-model="selected1" placeholder="选择部门" style="width: 300px;">
        <el-option label="生产部" value="1">生产部</el-option>
        <el-option label="技术部" value="2">技术部</el-option>
        <el-option label="质量部" value="3">质量部</el-option>
      </el-select>
      <span style="margin-left: 10px;">选中: {{ selected1 }}</span>
    </div>

    <div style="margin: 20px 0;">
      <h3>测试2: 使用数组循环</h3>
      <el-select v-model="selected2" placeholder="选择部门" style="width: 300px;">
        <el-option
          v-for="dept in testDepts"
          :key="dept.id"
          :label="dept.name"
          :value="dept.id"
        >
          {{ dept.name }}
        </el-option>
      </el-select>
      <span style="margin-left: 10px;">选中: {{ selected2 }}</span>
    </div>

    <div style="margin: 20px 0;">
      <h3>测试3: 使用响应式数据</h3>
      <el-select v-model="selected3" placeholder="选择部门" style="width: 300px;">
        <el-option
          v-for="dept in departments"
          :key="dept.id"
          :label="dept.name"
          :value="dept.id"
        >
          {{ dept.name }}
        </el-option>
      </el-select>
      <span style="margin-left: 10px;">选中: {{ selected3 }}</span>
    </div>

    <div style="margin: 20px 0;">
      <h3>数据状态</h3>
      <p>testDepts 长度: {{ testDepts.length }}</p>
      <p>departments 长度: {{ departments.length }}</p>
      <p>departments 内容: {{ JSON.stringify(departments) }}</p>
    </div>

    <div style="margin: 20px 0;">
      <el-button @click="loadData" type="primary">加载数据</el-button>
      <el-button @click="clearData" type="danger">清空数据</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const selected1 = ref('')
const selected2 = ref('')
const selected3 = ref('')

// 静态数据
const testDepts = [
  { id: 1, name: '生产部' },
  { id: 2, name: '技术部' },
  { id: 3, name: '质量部' }
]

// 响应式数据
const departments = ref([])

const loadData = () => {
  console.log('加载数据...')
  departments.value = [
    { id: 1, name: '生产部' },
    { id: 2, name: '技术部' },
    { id: 3, name: '质量部' },
    { id: 4, name: '安全部' },
    { id: 5, name: '设备部' }
  ]
  console.log('数据加载完成:', departments.value)
}

const clearData = () => {
  departments.value = []
  console.log('数据已清空')
}

onMounted(() => {
  console.log('组件挂载')
  loadData()
})
</script>
