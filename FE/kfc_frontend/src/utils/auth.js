/**
 * 认证相关工具函数
 */

// 获取token
export const getToken = () => {
  return localStorage.getItem('token')
}

// 设置token
export const setToken = (token) => {
  localStorage.setItem('token', token)
}

// 移除token
export const removeToken = () => {
  localStorage.removeItem('token')
}

// 获取用户角色
export const getUserRole = () => {
  return localStorage.getItem('role')
}

// 设置用户角色
export const setUserRole = (role) => {
  localStorage.setItem('role', role)
}

// 移除用户角色
export const removeUserRole = () => {
  localStorage.removeItem('role')
}

// 清除所有认证信息
export const clearAuth = () => {
  removeToken()
  removeUserRole()
}

// 检查是否已认证
export const isAuthenticated = () => {
  return !!getToken()
}

// 检查是否为店员
export const isStaff = () => {
  return getUserRole() === 'staff'
}