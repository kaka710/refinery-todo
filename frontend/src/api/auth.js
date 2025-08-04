import { request } from '@/utils/request'

// 用户认证相关API

/**
 * 用户登录
 * @param {object} data 登录数据
 * @param {string} data.username 用户名或工号
 * @param {string} data.password 密码
 * @returns {Promise}
 */
export function login(data) {
  return request.post('/v1/auth/login/', data)
}

/**
 * 用户登出
 * @param {object} data 登出数据
 * @param {string} data.refresh 刷新token
 * @returns {Promise}
 */
export function logout(data) {
  return request.post('/v1/auth/logout/', data)
}

/**
 * 刷新token
 * @param {object} data 刷新数据
 * @param {string} data.refresh 刷新token
 * @returns {Promise}
 */
export function refreshToken(data) {
  return request.post('/v1/auth/token/refresh/', data)
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getUserInfo() {
  return request.get('/v1/auth/users/me/')
}

/**
 * 获取用户权限信息
 * @returns {Promise}
 */
export function getUserPermissions() {
  return request.get('/v1/auth/permissions/')
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
  return request.post('/v1/auth/users/change_password/', data)
}

/**
 * 更新用户资料
 * @param {object} data 用户资料数据
 * @returns {Promise}
 */
export function updateProfile(data) {
  return request.put('/v1/auth/users/update_profile/', data)
}

/**
 * 用户注册（管理员功能）
 * @param {object} data 注册数据
 * @returns {Promise}
 */
export function register(data) {
  return request.post('/v1/auth/register/', data)
}

/**
 * 获取用户列表
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getUserList(params) {
  return request.get('/v1/auth/users/', { params })
}

/**
 * 获取用户详情
 * @param {number} id 用户ID
 * @returns {Promise}
 */
export function getUserDetail(id) {
  return request.get(`/v1/auth/users/${id}/`)
}

/**
 * 更新用户信息
 * @param {number} id 用户ID
 * @param {object} data 用户数据
 * @returns {Promise}
 */
export function updateUser(id, data) {
  return request.put(`/v1/auth/users/${id}/`, data)
}

/**
 * 创建用户
 * @param {object} data 用户数据
 * @returns {Promise}
 */
export function createUser(data) {
  return request.post('/v1/auth/users/', data)
}

/**
 * 删除用户
 * @param {number} id 用户ID
 * @returns {Promise}
 */
export function deleteUser(id) {
  return request.delete(`/v1/auth/users/${id}/`)
}

/**
 * 激活用户
 * @param {number} id 用户ID
 * @returns {Promise}
 */
export function activateUser(id) {
  return request.post(`/v1/auth/users/${id}/activate/`)
}

/**
 * 停用用户
 * @param {number} id 用户ID
 * @returns {Promise}
 */
export function deactivateUser(id) {
  return request.post(`/v1/auth/users/${id}/deactivate/`)
}

/**
 * 获取登录日志
 * @param {object} params 查询参数
 * @returns {Promise}
 */
export function getLoginLogs(params) {
  return request.get('/v1/auth/login-logs/', { params })
}
