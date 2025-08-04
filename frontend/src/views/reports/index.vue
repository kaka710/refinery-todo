<template>
  <div class="reports">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><DataAnalysis /></el-icon>
            统计报表
          </h1>
          <p class="page-subtitle">任务管理数据分析与统计报表</p>
        </div>
        <div class="header-right">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateRangeChange"
            size="large"
            style="margin-right: 12px"
          />
          <el-button type="primary" @click="handleExport" size="large">
            <el-icon><Download /></el-icon>
            导出报表
          </el-button>
        </div>
      </div>
    </div>

    <!-- 实时统计卡片 -->
    <div class="stats-overview">
      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon total-tasks">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ realTimeStats.total_tasks || 0 }}</div>
                <div class="stats-label">总任务数</div>
                <div class="stats-change positive">
                  <el-icon><ArrowUp /></el-icon>
                  +{{ realTimeStats.tasks_increase || 0 }}
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon completed-tasks">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ realTimeStats.completed_tasks || 0 }}</div>
                <div class="stats-label">已完成任务</div>
                <div class="stats-change positive">
                  <el-icon><ArrowUp /></el-icon>
                  +{{ realTimeStats.completed_increase || 0 }}
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon completion-rate">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ realTimeStats.completion_rate || 0 }}%</div>
                <div class="stats-label">完成率</div>
                <div class="stats-change positive">
                  <el-icon><ArrowUp /></el-icon>
                  +{{ realTimeStats.rate_increase || 0 }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-card class="stats-card" shadow="never">
            <div class="stats-content">
              <div class="stats-icon overdue-tasks">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ realTimeStats.overdue_tasks || 0 }}</div>
                <div class="stats-label">逾期任务</div>
                <div class="stats-change negative">
                  <el-icon><ArrowDown /></el-icon>
                  -{{ realTimeStats.overdue_decrease || 0 }}
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <el-row :gutter="24">
        <!-- 任务完成趋势 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="chart-card" shadow="never">
            <template #header>
              <div class="chart-header">
                <span>任务完成趋势</span>
                <el-select v-model="trendPeriod" size="small" style="width: 100px">
                  <el-option label="日" value="daily" />
                  <el-option label="周" value="weekly" />
                  <el-option label="月" value="monthly" />
                </el-select>
              </div>
            </template>
            <div class="chart-container">
              <v-chart
                v-if="taskTrendOption && Object.keys(taskTrendOption).length > 0"
                :option="taskTrendOption"
                :loading="chartLoading.trend"
                style="height: 300px"
                :key="'trend-chart'"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 任务状态分布 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="chart-card" shadow="never">
            <template #header>
              <span>任务状态分布</span>
            </template>
            <div class="chart-container">
              <v-chart
                v-if="taskStatusOption && Object.keys(taskStatusOption).length > 0"
                :option="taskStatusOption"
                :loading="chartLoading.status"
                style="height: 300px"
                :key="'status-chart'"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 部门工作量对比 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="chart-card" shadow="never">
            <template #header>
              <span>部门工作量对比</span>
            </template>
            <div class="chart-container">
              <v-chart
                v-if="departmentWorkloadOption && Object.keys(departmentWorkloadOption).length > 0"
                :option="departmentWorkloadOption"
                :loading="chartLoading.workload"
                style="height: 300px"
                :key="'workload-chart'"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 任务优先级分布 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="chart-card" shadow="never">
            <template #header>
              <span>任务优先级分布</span>
            </template>
            <div class="chart-container">
              <v-chart
                v-if="taskPriorityOption && Object.keys(taskPriorityOption).length > 0"
                :option="taskPriorityOption"
                :loading="chartLoading.priority"
                style="height: 300px"
                :key="'priority-chart'"
              />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 详细数据表格 -->
    <div class="data-tables">
      <el-row :gutter="24">
        <!-- 用户绩效排行 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="table-card" shadow="never">
            <template #header>
              <div class="table-header">
                <span>用户绩效排行</span>
                <el-button size="small" @click="loadUserPerformance">
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </div>
            </template>
            <el-table
              :data="userPerformanceData"
              v-loading="tableLoading.performance"
              style="width: 100%"
              size="small"
            >
              <el-table-column type="index" label="排名" width="60" />
              <el-table-column prop="user_name" label="姓名" width="100" />
              <el-table-column prop="department_name" label="部门" width="100" />
              <el-table-column prop="completed_tasks" label="完成任务" width="80" align="center" />
              <el-table-column prop="completion_rate" label="完成率" width="80" align="center">
                <template #default="{ row }">
                  <el-tag :type="getPerformanceTagType(row.completion_rate)" size="small">
                    {{ row.completion_rate }}%
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="avg_completion_time" label="平均用时" align="center">
                <template #default="{ row }">
                  {{ row.avg_completion_time }}天
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <!-- 逾期任务列表 -->
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-card class="table-card" shadow="never">
            <template #header>
              <div class="table-header">
                <span>逾期任务列表</span>
                <el-button size="small" @click="loadOverdueTasks">
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </div>
            </template>
            <el-table
              :data="overdueTasksData"
              v-loading="tableLoading.overdue"
              style="width: 100%"
              size="small"
            >
              <el-table-column prop="title" label="任务标题" min-width="120" show-overflow-tooltip />
              <el-table-column prop="assignee_name" label="负责人" width="80" />
              <el-table-column prop="due_date" label="截止日期" width="100" />
              <el-table-column prop="overdue_days" label="逾期天数" width="80" align="center">
                <template #default="{ row }">
                  <el-tag type="danger" size="small">
                    {{ row.overdue_days }}天
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="60" align="center">
                <template #default="{ row }">
                  <el-button size="small" type="primary" link @click="viewTask(row.id)">
                    查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  DataAnalysis, Download, Document, CircleCheck, TrendCharts, Warning,
  ArrowUp, ArrowDown, Refresh
} from '@element-plus/icons-vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import * as echarts from 'echarts/core'
import VChart from 'vue-echarts'
import {
  getTaskOverview,
  getTaskCompletionRate,
  getDepartmentWorkload,
  getUserPerformance,
  getTaskPriorityDistribution,
  getTaskStatusDistribution,
  getTaskTrend,
  getOverdueTasks,
  exportReport,
  getRealTimeStats
} from '@/api/reports'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const router = useRouter()

// 响应式数据
const dateRange = ref([])
const trendPeriod = ref('daily')
const realTimeStats = ref({})
const userPerformanceData = ref([])
const overdueTasksData = ref([])

// 加载状态
const chartLoading = reactive({
  trend: false,
  status: false,
  workload: false,
  priority: false
})

const tableLoading = reactive({
  performance: false,
  overdue: false
})

// 图表配置
const taskTrendOption = ref(null)
const taskStatusOption = ref(null)
const departmentWorkloadOption = ref(null)
const taskPriorityOption = ref(null)

// 模拟数据
const mockRealTimeStats = {
  total_tasks: 156,
  completed_tasks: 98,
  completion_rate: 62.8,
  overdue_tasks: 12,
  tasks_increase: 8,
  completed_increase: 15,
  rate_increase: 3.2,
  overdue_decrease: 2
}

const mockUserPerformance = [
  {
    user_name: '张三',
    department_name: '技术部',
    completed_tasks: 25,
    completion_rate: 95.2,
    avg_completion_time: 2.3
  },
  {
    user_name: '李四',
    department_name: '生产部',
    completed_tasks: 22,
    completion_rate: 88.0,
    avg_completion_time: 3.1
  },
  {
    user_name: '王五',
    department_name: '质量部',
    completed_tasks: 20,
    completion_rate: 83.3,
    avg_completion_time: 2.8
  },
  {
    user_name: '赵六',
    department_name: '技术部',
    completed_tasks: 18,
    completion_rate: 78.3,
    avg_completion_time: 3.5
  },
  {
    user_name: '钱七',
    department_name: '生产部',
    completed_tasks: 16,
    completion_rate: 72.7,
    avg_completion_time: 4.2
  }
]

const mockOverdueTasks = [
  {
    id: 1,
    title: '设备维护检查报告',
    assignee_name: '张三',
    due_date: '2024-01-10',
    overdue_days: 5
  },
  {
    id: 2,
    title: '月度安全培训总结',
    assignee_name: '李四',
    due_date: '2024-01-12',
    overdue_days: 3
  },
  {
    id: 3,
    title: '生产线效率分析',
    assignee_name: '王五',
    due_date: '2024-01-13',
    overdue_days: 2
  },
  {
    id: 4,
    title: '质量控制流程优化',
    assignee_name: '赵六',
    due_date: '2024-01-14',
    overdue_days: 1
  }
]

// 初始化日期范围（最近30天）
const initDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)

  dateRange.value = [
    start.toISOString().split('T')[0],
    end.toISOString().split('T')[0]
  ]
}

// 加载实时统计数据
const loadRealTimeStats = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    realTimeStats.value = mockRealTimeStats
  } catch (error) {
    console.error('加载实时统计失败:', error)
    ElMessage.error('加载实时统计失败')
  }
}

// 加载任务趋势数据
const loadTaskTrend = async () => {
  chartLoading.trend = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 模拟趋势数据
    const dates = []
    const completedData = []
    const createdData = []

    for (let i = 6; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      dates.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }))
      completedData.push(Math.floor(Math.random() * 20) + 10)
      createdData.push(Math.floor(Math.random() * 25) + 15)
    }

    taskTrendOption.value = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['新建任务', '完成任务']
      },
      xAxis: {
        type: 'category',
        data: dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '新建任务',
          type: 'line',
          data: createdData,
          smooth: true,
          itemStyle: {
            color: '#3b82f6'
          }
        },
        {
          name: '完成任务',
          type: 'line',
          data: completedData,
          smooth: true,
          itemStyle: {
            color: '#10b981'
          }
        }
      ]
    }
  } catch (error) {
    console.error('加载任务趋势失败:', error)
    ElMessage.error('加载任务趋势失败')
  } finally {
    chartLoading.trend = false
  }
}

// 加载任务状态分布
const loadTaskStatus = async () => {
  chartLoading.status = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 400))

    const statusData = [
      { value: 45, name: '进行中' },
      { value: 32, name: '已完成' },
      { value: 18, name: '待开始' },
      { value: 12, name: '已逾期' },
      { value: 8, name: '已取消' }
    ]

    taskStatusOption.value = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '任务状态',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 20,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: statusData,
          color: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6b7280']
        }
      ]
    }
  } catch (error) {
    console.error('加载任务状态失败:', error)
    ElMessage.error('加载任务状态失败')
  } finally {
    chartLoading.status = false
  }
}

// 加载部门工作量
const loadDepartmentWorkload = async () => {
  chartLoading.workload = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 450))

    const departments = ['技术部', '生产部', '质量部', '安全部', '管理部']
    const workloadData = [85, 72, 68, 45, 38]

    departmentWorkloadOption.value = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: departments,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '任务数量'
      },
      series: [
        {
          name: '任务数量',
          type: 'bar',
          data: workloadData,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#3b82f6' },
              { offset: 1, color: '#1d4ed8' }
            ])
          },
          barWidth: '60%'
        }
      ]
    }
  } catch (error) {
    console.error('加载部门工作量失败:', error)
    ElMessage.error('加载部门工作量失败')
  } finally {
    chartLoading.workload = false
  }
}

// 加载任务优先级分布
const loadTaskPriority = async () => {
  chartLoading.priority = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 350))

    const priorityData = [
      { value: 28, name: '高优先级' },
      { value: 45, name: '中优先级' },
      { value: 32, name: '低优先级' }
    ]

    taskPriorityOption.value = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        bottom: '5%',
        left: 'center'
      },
      series: [
        {
          name: '任务优先级',
          type: 'pie',
          radius: ['30%', '60%'],
          center: ['50%', '45%'],
          data: priorityData,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          color: ['#ef4444', '#f59e0b', '#10b981']
        }
      ]
    }
  } catch (error) {
    console.error('加载任务优先级失败:', error)
    ElMessage.error('加载任务优先级失败')
  } finally {
    chartLoading.priority = false
  }
}

// 加载用户绩效数据
const loadUserPerformance = async () => {
  tableLoading.performance = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 400))
    userPerformanceData.value = mockUserPerformance
  } catch (error) {
    console.error('加载用户绩效失败:', error)
    ElMessage.error('加载用户绩效失败')
  } finally {
    tableLoading.performance = false
  }
}

// 加载逾期任务数据
const loadOverdueTasks = async () => {
  tableLoading.overdue = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 350))
    overdueTasksData.value = mockOverdueTasks
  } catch (error) {
    console.error('加载逾期任务失败:', error)
    ElMessage.error('加载逾期任务失败')
  } finally {
    tableLoading.overdue = false
  }
}

// 事件处理
const handleDateRangeChange = (dates) => {
  if (dates && dates.length === 2) {
    // 重新加载所有数据
    loadAllData()
  }
}

const handleExport = async () => {
  try {
    ElMessage.info('正在生成报表，请稍候...')

    // 模拟导出
    await new Promise(resolve => setTimeout(resolve, 2000))

    // 创建一个虚拟的下载链接
    const link = document.createElement('a')
    link.href = 'data:text/plain;charset=utf-8,统计报表数据导出成功'
    link.download = `统计报表_${new Date().toISOString().split('T')[0]}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    ElMessage.success('报表导出成功')
  } catch (error) {
    console.error('导出报表失败:', error)
    ElMessage.error('导出报表失败')
  }
}

const viewTask = (taskId) => {
  router.push(`/tasks/${taskId}`)
}

// 工具方法
const getPerformanceTagType = (rate) => {
  if (rate >= 90) return 'success'
  if (rate >= 80) return 'primary'
  if (rate >= 70) return 'warning'
  return 'danger'
}

// 加载所有数据
const loadAllData = () => {
  loadRealTimeStats()
  loadTaskTrend()
  loadTaskStatus()
  loadDepartmentWorkload()
  loadTaskPriority()
  loadUserPerformance()
  loadOverdueTasks()
}

// 监听趋势周期变化
watch(trendPeriod, () => {
  loadTaskTrend()
})

// 生命周期
onMounted(() => {
  // 初始化图表配置为空对象，避免null引用
  taskTrendOption.value = {}
  taskStatusOption.value = {}
  departmentWorkloadOption.value = {}
  taskPriorityOption.value = {}

  initDateRange()
  loadAllData()
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理图表配置
  taskTrendOption.value = null
  taskStatusOption.value = null
  departmentWorkloadOption.value = null
  taskPriorityOption.value = null
})
</script>

<style scoped>
.reports {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left .page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
}

.header-left .page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 统计概览 */
.stats-overview {
  margin-bottom: 24px;
}

.stats-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.stats-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stats-icon.total-tasks {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.stats-icon.completed-tasks {
  background: linear-gradient(135deg, #10b981, #047857);
}

.stats-icon.completion-rate {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.stats-icon.overdue-tasks {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stats-label {
  font-size: 14px;
  color: #6b7280;
  margin: 4px 0;
}

.stats-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stats-change.positive {
  color: #10b981;
}

.stats-change.negative {
  color: #ef4444;
}

/* 图表区域 */
.charts-section {
  margin-bottom: 24px;
}

.chart-card,
.table-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.chart-header,
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1f2937;
}

.chart-container {
  padding: 16px 0;
}

/* 数据表格 */
.data-tables {
  margin-bottom: 24px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f8fafc;
  color: #374151;
  font-weight: 600;
}

:deep(.el-table td) {
  border-bottom: 1px solid #f1f5f9;
}

:deep(.el-table tr:hover > td) {
  background-color: #f8faff;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .charts-section .el-col,
  .data-tables .el-col {
    margin-bottom: 24px;
  }
}

@media (max-width: 768px) {
  .reports {
    padding: 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .header-right {
    flex-direction: column;
    gap: 12px;
  }

  .stats-content {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }

  .stats-info {
    text-align: center;
  }

  .chart-header,
  .table-header {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }
}

/* 图表样式优化 */
:deep(.echarts) {
  border-radius: 8px;
}

/* 加载状态 */
:deep(.el-loading-mask) {
  border-radius: 8px;
}

/* 表格操作按钮 */
:deep(.el-button--small) {
  padding: 4px 8px;
  font-size: 12px;
}

/* 标签样式 */
:deep(.el-tag--small) {
  font-size: 11px;
  padding: 2px 6px;
}
</style>
