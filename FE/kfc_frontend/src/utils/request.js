import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 错误修正：创建 axios 实例应使用 axios.create()，而非 axios.post()
const request = axios.create({
  baseURL: '/api', // 后端基础地址
  timeout: 30000 // 请求超时时间（30秒）
})

// 请求拦截器：携带 DRF Token（格式为 "Token {token}"）
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      // 为请求头添加 Authorization 字段，符合 DRF Token 认证格式
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    // 请求发送失败时的处理
    ElMessage.error('请求发送失败，请检查网络')
    return Promise.reject(error)
  }
)

// 响应拦截器：处理响应数据和错误
request.interceptors.response.use(
  (response) => {
    // 直接返回响应体中的 data 部分（简化业务层获取数据的逻辑）
    return response.data
  },
  (error) => {
    if (error.response) {
      // 处理有响应的错误（后端返回了错误状态码）
      const status = error.response.status
      const errorData = error.response.data

      if (status === 401) {
        // 401 未授权：清除本地存储的 token 和角色，跳转至登录页
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        router.push('/api/auth/users/login/')
        ElMessage.error('登录已过期，请重新登录')
      } else if (status === 400) {
        // 400 错误请求：通常是参数错误，显示后端返回的具体信息
        ElMessage.error(errorData.message || '参数错误，请检查输入')
      } else if (status === 404) {
        // 404 资源不存在
        ElMessage.error('请求的资源不存在')
      } else if (status >= 500) {
        // 5xx 服务器错误
        ElMessage.error('服务器内部错误，请稍后重试')
      } else {
        // 其他状态码的错误
        ElMessage.error(errorData.message || '操作失败')
      }
    } else {
      // 无响应的错误（如网络中断、跨域问题等）
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default request