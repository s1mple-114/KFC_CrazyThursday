import { createRouter, createWebHistory } from 'vue-router'
// 导入Login和Menu组件
import Login from '../views/coustomer/Login.vue'
import Menu from '../views/coustomer/Menu.vue'

// 路由规则：包含登录页和菜单页
const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/menu', // 菜单页的访问路径
    name: 'Menu',
    component: Menu
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router