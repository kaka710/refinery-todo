/**
 * ECharts 配置文件
 * 统一管理 ECharts 的导入和注册
 */

import { use } from 'echarts/core'

// 渲染器
import { CanvasRenderer } from 'echarts/renderers'

// 图表类型
import { 
  LineChart, 
  BarChart, 
  PieChart, 
  ScatterChart,
  RadarChart 
} from 'echarts/charts'

// 组件
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  DatasetComponent
} from 'echarts/components'

// 注册必要的组件
use([
  // 渲染器
  CanvasRenderer,
  
  // 图表
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  RadarChart,
  
  // 组件
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  DatasetComponent
])

// 导出 vue-echarts
export { default as VChart } from 'vue-echarts'

// 导出主题键
export { THEME_KEY } from 'vue-echarts'

// 默认图表配置
export const defaultChartOptions = {
  // 全局配置
  backgroundColor: 'transparent',
  
  // 标题配置
  title: {
    textStyle: {
      color: '#333',
      fontSize: 16,
      fontWeight: 'normal'
    }
  },
  
  // 提示框配置
  tooltip: {
    backgroundColor: 'rgba(50, 50, 50, 0.9)',
    borderColor: '#333',
    borderWidth: 1,
    textStyle: {
      color: '#fff',
      fontSize: 12
    }
  },
  
  // 图例配置
  legend: {
    textStyle: {
      color: '#666',
      fontSize: 12
    }
  },
  
  // 网格配置
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  }
}

// 饼图默认配置
export const defaultPieOptions = {
  ...defaultChartOptions,
  tooltip: {
    ...defaultChartOptions.tooltip,
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    ...defaultChartOptions.legend,
    orient: 'vertical',
    left: 'left'
  }
}

// 柱状图默认配置
export const defaultBarOptions = {
  ...defaultChartOptions,
  tooltip: {
    ...defaultChartOptions.tooltip,
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    axisLine: {
      lineStyle: {
        color: '#ddd'
      }
    },
    axisLabel: {
      color: '#666'
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      lineStyle: {
        color: '#ddd'
      }
    },
    axisLabel: {
      color: '#666'
    },
    splitLine: {
      lineStyle: {
        color: '#f0f0f0'
      }
    }
  }
}

// 折线图默认配置
export const defaultLineOptions = {
  ...defaultChartOptions,
  tooltip: {
    ...defaultChartOptions.tooltip,
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    axisLine: {
      lineStyle: {
        color: '#ddd'
      }
    },
    axisLabel: {
      color: '#666'
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      lineStyle: {
        color: '#ddd'
      }
    },
    axisLabel: {
      color: '#666'
    },
    splitLine: {
      lineStyle: {
        color: '#f0f0f0'
      }
    }
  }
}

// 颜色主题
export const chartColors = [
  '#409EFF', // 主蓝色
  '#67C23A', // 成功绿
  '#E6A23C', // 警告橙
  '#F56C6C', // 危险红
  '#909399', // 信息灰
  '#9C27B0', // 紫色
  '#FF9800', // 橙色
  '#4CAF50', // 绿色
  '#2196F3', // 蓝色
  '#FF5722'  // 深橙色
]
