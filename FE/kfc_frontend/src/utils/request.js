import axios from 'axios';

// 创建axios实例
const service = axios.create({
  baseURL: 'https://wkpgptfg-8000.asse.devtunnels.ms', // 后端接口基础地址
  timeout: 5000 // 请求超时时间
});

// 请求拦截器：添加Token到请求头
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // 根据后端要求的认证格式设置，这里假设是Bearer Token
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器：处理通用响应逻辑
service.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    // 可以在这里统一处理错误，比如Token过期跳转登录页等
    return Promise.reject(error);
  }
);

export default service;