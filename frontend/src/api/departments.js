/**
 * 部门相关API
 */
import request from '@/utils/request'

// 部门API
export const departmentsApi = {
  /**
   * 获取部门列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getDepartments(params = {}) {
    return request({
      url: '/v1/departments/departments/',
      method: 'get',
      params
    })
  },

  /**
   * 获取部门树形结构
   * @returns {Promise}
   */
  getDepartmentTree() {
    return request({
      url: '/v1/departments/departments/tree/',
      method: 'get'
    })
  },

  /**
   * 获取部门详情
   * @param {number} id - 部门ID
   * @returns {Promise}
   */
  getDepartment(id) {
    return request({
      url: `/v1/departments/departments/${id}/`,
      method: 'get'
    })
  },

  /**
   * 获取部门用户列表
   * @param {number} departmentId - 部门ID
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getDepartmentUsers(departmentId, params = {}) {
    return request({
      url: `/v1/departments/departments/${departmentId}/users/`,
      method: 'get',
      params
    })
  },

  /**
   * 创建部门
   * @param {Object} data - 部门数据
   * @returns {Promise}
   */
  createDepartment(data) {
    return request({
      url: '/v1/departments/departments/',
      method: 'post',
      data
    })
  },

  /**
   * 更新部门
   * @param {number} id - 部门ID
   * @param {Object} data - 部门数据
   * @returns {Promise}
   */
  updateDepartment(id, data) {
    return request({
      url: `/v1/departments/departments/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除部门
   * @param {number} id - 部门ID
   * @returns {Promise}
   */
  deleteDepartment(id) {
    return request({
      url: `/v1/departments/departments/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 获取部门统计信息
   * @param {number} id - 部门ID
   * @returns {Promise}
   */
  getDepartmentStats(id) {
    return request({
      url: `/v1/departments/departments/${id}/stats/`,
      method: 'get'
    })
  }
}

// 专业API
export const professionsApi = {
  /**
   * 获取专业列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getProfessions(params = {}) {
    return request({
      url: '/v1/departments/professions/',
      method: 'get',
      params
    })
  },

  /**
   * 获取专业详情
   * @param {number} id - 专业ID
   * @returns {Promise}
   */
  getProfession(id) {
    return request({
      url: `/v1/departments/professions/${id}/`,
      method: 'get'
    })
  },

  /**
   * 获取专业用户列表
   * @param {number} professionId - 专业ID
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getProfessionUsers(professionId, params = {}) {
    return request({
      url: `/v1/departments/professions/${professionId}/users/`,
      method: 'get',
      params
    })
  },

  /**
   * 创建专业
   * @param {Object} data - 专业数据
   * @returns {Promise}
   */
  createProfession(data) {
    return request({
      url: '/v1/departments/professions/',
      method: 'post',
      data
    })
  },

  /**
   * 更新专业
   * @param {number} id - 专业ID
   * @param {Object} data - 专业数据
   * @returns {Promise}
   */
  updateProfession(id, data) {
    return request({
      url: `/v1/departments/professions/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除专业
   * @param {number} id - 专业ID
   * @returns {Promise}
   */
  deleteProfession(id) {
    return request({
      url: `/v1/departments/professions/${id}/`,
      method: 'delete'
    })
  }
}

// 用户API
export const usersApi = {
  /**
   * 获取用户列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getUsers(params = {}) {
    return request({
      url: '/v1/auth/users/',
      method: 'get',
      params
    })
  },

  /**
   * 根据部门获取用户列表
   * @param {number} departmentId - 部门ID
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getUsersByDepartment(departmentId, params = {}) {
    return request({
      url: '/v1/auth/users/',
      method: 'get',
      params: {
        department: departmentId,
        ...params
      }
    })
  },

  /**
   * 获取用户详情
   * @param {number} id - 用户ID
   * @returns {Promise}
   */
  getUser(id) {
    return request({
      url: `/v1/auth/users/${id}/`,
      method: 'get'
    })
  },

  /**
   * 获取当前用户信息
   * @returns {Promise}
   */
  getCurrentUser() {
    return request({
      url: '/v1/auth/users/me/',
      method: 'get'
    })
  }
}

export default {
  departmentsApi,
  professionsApi,
  usersApi
}
