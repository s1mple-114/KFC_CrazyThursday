import { createRouter, createWebHistory } from 'vue-router'
// 引入页面组件
import Login from '../views/coustomer/Login.vue'
// 后面会加“菜单页”“订单页”等，先放登录页

// 路由规则：路径对应页面
const routes = [
  {
    path: '/',          // 默认路径（打开项目先显示登录页）
    name: 'Login',
    component: Login
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router