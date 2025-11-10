import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router/index.js'

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
    // 返回完整响应对象，以便能获取订单ID等信息
    return response
  },
  (error) => {
    if (error.response) {
      // 处理有响应的错误（后端返回了错误状态码）
      const status = error.response.status
      const errorData = error.response.data

      if (status === 401) {
        // 检查是否在演示模式下或者是否是关键流程页面（如支付流程）
        // 从当前URL判断是否在支付相关页面
        const currentPath = window.location.pathname;
        const isPaymentFlow = currentPath.includes('/order-submit') || currentPath.includes('/payment');
        
        // 如果不是在支付流程中，并且不是演示模式，则清除登录状态并重定向
        if (!isPaymentFlow) {
          localStorage.removeItem('token')
          localStorage.removeItem('role')
          router.push('/login')
          ElMessage.error('登录已过期，请重新登录')
        } else {
          // 在支付流程中，不清除登录状态，只显示警告信息
          console.warn('API认证失败，但在支付流程中保留登录状态')
          // 不跳转到登录页，让页面可以继续使用模拟数据
        }
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