import { request } from '@/utils/request'

// 通知相关API

/**
 * 获取通知列表
 * @param {object} params 查询参数
 * @param {number} params.page 页码
 * @param {number} params.page_size 每页数量
 * @param {string} params.type 通知类型
 * @param {boolean} params.is_read 是否已读
 * @returns {Promise}
 */
export function getNotifications(params = {}) {
  return request.get('/v1/notifications/', params)
}

/**
 * 获取通知详情
 * @param {number} id 通知ID
 * @returns {Promise}
 */
export function getNotificationDetail(id) {
  return request.get(`/v1/notifications/${id}/`)
}

/**
 * 标记通知为已读
 * @param {number} id 通知ID
 * @returns {Promise}
 */
export function markAsRead(id) {
  return request.patch(`/v1/notifications/${id}/`, { is_read: true })
}

/**
 * 批量标记通知为已读
 * @param {array} ids 通知ID数组
 * @returns {Promise}
 */
export function batchMarkAsRead(ids) {
  return request.post('/v1/notifications/batch_mark_read/', { ids })
}

/**
 * 标记所有通知为已读
 * @returns {Promise}
 */
export function markAllAsRead() {
  return request.post('/v1/notifications/mark_all_read/')
}

/**
 * 删除通知
 * @param {number} id 通知ID
 * @returns {Promise}
 */
export function deleteNotification(id) {
  return request.delete(`/v1/notifications/${id}/`)
}

/**
 * 批量删除通知
 * @param {array} ids 通知ID数组
 * @returns {Promise}
 */
export function batchDeleteNotifications(ids) {
  return request.post('/v1/notifications/batch_delete/', { ids })
}

/**
 * 获取未读通知数量
 * @returns {Promise}
 */
export function getUnreadCount() {
  return request.get('/v1/notifications/unread_count/')
}

/**
 * 获取通知统计信息
 * @returns {Promise}
 */
export function getNotificationStats() {
  return request.get('/v1/notifications/stats/')
}

/**
 * 创建通知（管理员功能）
 * @param {object} data 通知数据
 * @param {string} data.title 通知标题
 * @param {string} data.content 通知内容
 * @param {string} data.type 通知类型
 * @param {array} data.recipients 接收者ID数组
 * @returns {Promise}
 */
export function createNotification(data) {
  return request.post('/v1/notifications/', data)
}

/**
 * 发送系统通知（管理员功能）
 * @param {object} data 通知数据
 * @param {string} data.title 通知标题
 * @param {string} data.content 通知内容
 * @param {string} data.type 通知类型
 * @param {boolean} data.send_to_all 是否发送给所有用户
 * @param {array} data.departments 部门ID数组
 * @param {array} data.users 用户ID数组
 * @returns {Promise}
 */
export function sendSystemNotification(data) {
  return request.post('/v1/notifications/send_system/', data)
}
