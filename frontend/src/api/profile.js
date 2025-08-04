import { request } from '@/utils/request'

// 个人资料相关API

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getCurrentUser() {
  return request.get('/v1/auth/me/')
}

/**
 * 更新个人基本信息
 * @param {object} data 用户信息
 * @param {string} data.real_name 真实姓名
 * @param {string} data.email 邮箱
 * @param {string} data.phone 手机号
 * @param {string} data.position 职位
 * @param {string} data.office_location 办公地点
 * @returns {Promise}
 */
export function updateProfile(data) {
  return request.patch('/v1/auth/profile/', data)
}

/**
 * 修改密码
 * @param {object} data 密码数据
 * @param {string} data.old_password 旧密码
 * @param {string} data.new_password 新密码
 * @param {string} data.confirm_password 确认密码
 * @returns {Promise}
 */
export function changePassword(data) {
  return request.post('/v1/auth/change_password/', data)
}

/**
 * 上传头像
 * @param {FormData} formData 包含头像文件的表单数据
 * @returns {Promise}
 */
export function uploadAvatar(formData) {
  return request.upload('/v1/auth/upload_avatar/', formData)
}

/**
 * 删除头像
 * @returns {Promise}
 */
export function deleteAvatar() {
  return request.delete('/v1/auth/avatar/')
}

/**
 * 获取用户偏好设置
 * @returns {Promise}
 */
export function getUserPreferences() {
  return request.get('/v1/auth/preferences/')
}

/**
 * 更新用户偏好设置
 * @param {object} data 偏好设置
 * @param {string} data.theme 主题 (light/dark/auto)
 * @param {string} data.language 语言 (zh-CN/en-US)
 * @param {boolean} data.email_notifications 邮件通知
 * @param {boolean} data.sms_notifications 短信通知
 * @param {boolean} data.desktop_notifications 桌面通知
 * @returns {Promise}
 */
export function updateUserPreferences(data) {
  return request.patch('/v1/auth/preferences/', data)
}

/**
 * 获取用户活动日志
 * @param {object} params 查询参数
 * @param {number} params.page 页码
 * @param {number} params.page_size 每页数量
 * @param {string} params.action_type 操作类型
 * @returns {Promise}
 */
export function getUserActivityLog(params = {}) {
  return request.get('/v1/auth/activity_log/', params)
}

/**
 * 获取用户统计信息
 * @returns {Promise}
 */
export function getUserStats() {
  return request.get('/v1/auth/stats/')
}

/**
 * 绑定第三方账号
 * @param {object} data 绑定数据
 * @param {string} data.provider 提供商 (shihuatong/wechat)
 * @param {string} data.provider_id 第三方ID
 * @param {string} data.access_token 访问令牌
 * @returns {Promise}
 */
export function bindThirdPartyAccount(data) {
  return request.post('/v1/auth/bind_account/', data)
}

/**
 * 解绑第三方账号
 * @param {string} provider 提供商
 * @returns {Promise}
 */
export function unbindThirdPartyAccount(provider) {
  return request.delete(`/v1/auth/unbind_account/${provider}/`)
}

/**
 * 验证邮箱
 * @param {object} data 验证数据
 * @param {string} data.email 邮箱地址
 * @returns {Promise}
 */
export function sendEmailVerification(data) {
  return request.post('/v1/auth/send_email_verification/', data)
}

/**
 * 确认邮箱验证
 * @param {object} data 确认数据
 * @param {string} data.token 验证令牌
 * @returns {Promise}
 */
export function confirmEmailVerification(data) {
  return request.post('/v1/auth/confirm_email_verification/', data)
}

/**
 * 验证手机号
 * @param {object} data 验证数据
 * @param {string} data.phone 手机号
 * @returns {Promise}
 */
export function sendPhoneVerification(data) {
  return request.post('/v1/auth/send_phone_verification/', data)
}

/**
 * 确认手机号验证
 * @param {object} data 确认数据
 * @param {string} data.phone 手机号
 * @param {string} data.code 验证码
 * @returns {Promise}
 */
export function confirmPhoneVerification(data) {
  return request.post('/v1/auth/confirm_phone_verification/', data)
}
