import { createRouter, createWebHistory } from 'vue-router'
// 导入组件
import Login from '../views/coustomer/Login.vue'
import Menu from '../views/coustomer/Menu.vue'
// 导入店员页面组件
import StaffOrder from '../views/staff/StaffOrder.vue'
import StaffProduct from '../views/staff/StaffProduct.vue'

// 路由规则
const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/menu',
    name: 'Menu',
    component: Menu
  },
  // 店员相关路由
  {
    path: '/staff/order',
    name: 'StaffOrder',
    component: StaffOrder
  },
  {
    path: '/staff/product',
    name: 'StaffProduct',
    component: StaffProduct
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router