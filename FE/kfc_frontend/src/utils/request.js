import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: 'https://wkpgptfg-8000.asse.devtunnels.ms/', // 后端地址已修改
  timeout: 30000
})

// 请求拦截器：携带DRF Token（格式为 "Token {token}"）
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      // 关键修改 改为Token
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器保持不变（处理错误和Token过期）
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        router.push('/login')
        ElMessage.error('登录已过期，请重新登录')
      } else {
        ElMessage.error(error.response.data.message || '操作失败')
      }
    } else {
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default request