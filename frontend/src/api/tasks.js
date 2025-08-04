import { request } from '@/utils/request'

// 任务管理相关API

/**
 * 获取任务列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskList(params) {
  return request.get('/v1/tasks/tasks/', { params })
}

/**
 * 获取我的任务
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getMyTasks(params) {
  return request.get('/v1/tasks/tasks/my_tasks/', { params })
}

/**
 * 获取分配给我的任务
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getAssignedTasks(params) {
  return request.get('/v1/tasks/tasks/assigned_to_me/', { params })
}

/**
 * 获取我创建的任务
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getCreatedTasks(params) {
  return request.get('/v1/tasks/tasks/created_by_me/', { params })
}

/**
 * 获取逾期任务
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getOverdueTasks(params) {
  return request.get('/v1/tasks/tasks/overdue/', { params })
}

/**
 * 获取任务详情
 * @param {string} id 任务ID
 * @returns {Promise}
 */
export function getTaskDetail(id) {
  return request.get(`/v1/tasks/tasks/${id}/`)
}

/**
 * 创建任务
 * @param {object} data 任务数据
 * @returns {Promise}
 */
export function createTask(data) {
  return request.post('/v1/tasks/tasks/', data)
}

/**
 * 更新任务
 * @param {string} id 任务ID
 * @param {object} data 任务数据
 * @returns {Promise}
 */
export function updateTask(id, data) {
  return request.put(`/v1/tasks/tasks/${id}/`, data)
}

/**
 * 删除任务
 * @param {string} id 任务ID
 * @returns {Promise}
 */
export function deleteTask(id) {
  return request.delete(`/v1/tasks/tasks/${id}/`)
}

/**
 * 发布任务
 * @param {string} id 任务ID
 * @returns {Promise}
 */
export function publishTask(id) {
  return request.post(`/v1/tasks/tasks/${id}/publish/`)
}

/**
 * 取消任务
 * @param {string} id 任务ID
 * @returns {Promise}
 */
export function cancelTask(id) {
  return request.post(`/v1/tasks/tasks/${id}/cancel/`)
}

/**
 * 获取任务统计
 * @returns {Promise}
 */
export function getTaskStatistics() {
  return request.get('/v1/tasks/tasks/statistics/')
}

// 任务分配相关API

/**
 * 获取任务分配列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskAssignments(params) {
  return request.get('/v1/tasks/assignments/', { params })
}

/**
 * 接受任务分配
 * @param {number} id 分配ID
 * @returns {Promise}
 */
export function acceptAssignment(id) {
  return request.post(`/v1/tasks/assignments/${id}/accept/`)
}

/**
 * 拒绝任务分配
 * @param {number} id 分配ID
 * @returns {Promise}
 */
export function rejectAssignment(id) {
  return request.post(`/v1/tasks/assignments/${id}/reject/`)
}

/**
 * 完成任务分配
 * @param {number} id 分配ID
 * @returns {Promise}
 */
export function completeAssignment(id) {
  return request.post(`/v1/tasks/assignments/${id}/complete/`)
}

// 任务执行相关API

/**
 * 获取任务执行记录
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskExecutions(params) {
  return request.get('/v1/tasks/executions/', { params })
}

/**
 * 更新任务执行记录
 * @param {number} id 执行记录ID
 * @param {object} data 执行数据
 * @returns {Promise}
 */
export function updateTaskExecution(id, data) {
  return request.put(`/v1/tasks/executions/${id}/`, data)
}

/**
 * 开始执行任务
 * @param {number} id 执行记录ID
 * @returns {Promise}
 */
export function startExecution(id) {
  return request.post(`/v1/tasks/executions/${id}/start/`)
}

/**
 * 暂停执行任务
 * @param {number} id 执行记录ID
 * @returns {Promise}
 */
export function pauseExecution(id) {
  return request.post(`/v1/tasks/executions/${id}/pause/`)
}

/**
 * 恢复执行任务
 * @param {number} id 执行记录ID
 * @returns {Promise}
 */
export function resumeExecution(id) {
  return request.post(`/v1/tasks/executions/${id}/resume/`)
}

// 任务评价相关API

/**
 * 获取任务评价列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskReviews(params) {
  return request.get('/v1/tasks/reviews/', { params })
}

/**
 * 创建任务评价
 * @param {object} data 评价数据
 * @returns {Promise}
 */
export function createTaskReview(data) {
  return request.post('/v1/tasks/reviews/', data)
}

/**
 * 更新任务评价
 * @param {number} id 评价ID
 * @param {object} data 评价数据
 * @returns {Promise}
 */
export function updateTaskReview(id, data) {
  return request.put(`/v1/tasks/reviews/${id}/`, data)
}

// 任务附件相关API

/**
 * 获取任务附件列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskAttachments(params) {
  return request.get('/v1/tasks/attachments/', { params })
}

/**
 * 上传任务附件
 * @param {FormData} formData 文件数据
 * @returns {Promise}
 */
export function uploadTaskAttachment(formData) {
  return request.upload('/v1/tasks/attachments/', formData)
}

/**
 * 删除任务附件
 * @param {number} id 附件ID
 * @returns {Promise}
 */
export function deleteTaskAttachment(id) {
  return request.delete(`/v1/tasks/attachments/${id}/`)
}

// 任务评论相关API

/**
 * 获取任务评论列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskComments(params) {
  return request.get('/v1/tasks/comments/', { params })
}

/**
 * 创建任务评论
 * @param {object} data 评论数据
 * @returns {Promise}
 */
export function createTaskComment(data) {
  return request.post('/v1/tasks/comments/', data)
}

/**
 * 更新任务评论
 * @param {number} id 评论ID
 * @param {object} data 评论数据
 * @returns {Promise}
 */
export function updateTaskComment(id, data) {
  return request.put(`/v1/tasks/comments/${id}/`, data)
}

/**
 * 删除任务评论
 * @param {number} id 评论ID
 * @returns {Promise}
 */
export function deleteTaskComment(id) {
  return request.delete(`/v1/tasks/comments/${id}/`)
}

// 任务模板相关API

/**
 * 获取任务模板列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getTaskTemplates(params) {
  return request.get('/v1/tasks/templates/', { params })
}

/**
 * 获取任务模板详情
 * @param {number} id 模板ID
 * @returns {Promise}
 */
export function getTaskTemplate(id) {
  return request.get(`/v1/tasks/templates/${id}/`)
}

/**
 * 创建任务模板
 * @param {object} data 模板数据
 * @returns {Promise}
 */
export function createTaskTemplate(data) {
  return request.post('/v1/tasks/templates/', data)
}

/**
 * 更新任务模板
 * @param {number} id 模板ID
 * @param {object} data 模板数据
 * @returns {Promise}
 */
export function updateTaskTemplate(id, data) {
  return request.put(`/v1/tasks/templates/${id}/`, data)
}

/**
 * 删除任务模板
 * @param {number} id 模板ID
 * @returns {Promise}
 */
export function deleteTaskTemplate(id) {
  return request.delete(`/v1/tasks/templates/${id}/`)
}

/**
 * 使用模板创建任务
 * @param {number} id 模板ID
 * @param {object} data 任务数据
 * @returns {Promise}
 */
export function useTemplate(id, data) {
  return request.post(`/v1/tasks/templates/${id}/use_template/`, data)
}
