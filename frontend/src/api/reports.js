import { request } from '@/utils/request'

// 统计报表相关API

/**
 * 获取任务统计概览
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @param {number} params.department_id 部门ID
 * @returns {Promise}
 */
export function getTaskOverview(params = {}) {
  return request.get('/v1/reports/task_overview/', params)
}

/**
 * 获取任务完成率统计
 * @param {object} params 查询参数
 * @param {string} params.period 统计周期 (daily/weekly/monthly)
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function getTaskCompletionRate(params = {}) {
  return request.get('/v1/reports/task_completion_rate/', params)
}

/**
 * 获取部门工作量统计
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function getDepartmentWorkload(params = {}) {
  return request.get('/v1/reports/department_workload/', params)
}

/**
 * 获取用户绩效统计
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @param {number} params.department_id 部门ID
 * @param {number} params.limit 返回数量限制
 * @returns {Promise}
 */
export function getUserPerformance(params = {}) {
  return request.get('/v1/reports/user_performance/', params)
}

/**
 * 获取任务优先级分布
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function getTaskPriorityDistribution(params = {}) {
  return request.get('/v1/reports/task_priority_distribution/', params)
}

/**
 * 获取任务状态分布
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function getTaskStatusDistribution(params = {}) {
  return request.get('/v1/reports/task_status_distribution/', params)
}

/**
 * 获取任务趋势分析
 * @param {object} params 查询参数
 * @param {string} params.period 统计周期 (daily/weekly/monthly)
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function getTaskTrend(params = {}) {
  return request.get('/v1/reports/task_trend/', params)
}

/**
 * 获取逾期任务统计
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @param {number} params.department_id 部门ID
 * @returns {Promise}
 */
export function getOverdueTasks(params = {}) {
  return request.get('/v1/reports/overdue_tasks/', params)
}

/**
 * 导出报表数据
 * @param {object} params 导出参数
 * @param {string} params.report_type 报表类型
 * @param {string} params.format 导出格式 (excel/pdf)
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @returns {Promise}
 */
export function exportReport(params = {}) {
  return request.download('/v1/reports/export/', params)
}

/**
 * 获取实时统计数据
 * @returns {Promise}
 */
export function getRealTimeStats() {
  return request.get('/v1/reports/realtime_stats/')
}

/**
 * 获取工作效率分析
 * @param {object} params 查询参数
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @param {number} params.user_id 用户ID
 * @returns {Promise}
 */
export function getWorkEfficiency(params = {}) {
  return request.get('/v1/reports/work_efficiency/', params)
}
