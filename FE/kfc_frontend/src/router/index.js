import { createRouter, createWebHistory } from 'vue-router'
// 导入组件
import Login from '../views/coustomer/Login.vue'
import Menu from '../views/coustomer/Menu.vue'
 import Cart from '../views/coustomer/Cart.vue'
import OrderSubmit from '../views/coustomer/OrderSubmit.vue'
import OrderList from '../views/coustomer/OrderList.vue'
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
    component: Menu,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/order-submit',
    name: 'OrderSubmit',
    component: () => import('../views/coustomer/OrderSubmit.vue'),
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/payment',
    name: 'Payment',
    component: () => import('../views/coustomer/Payment.vue'),
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/order-list',
    name: 'OrderList',
    component: OrderList,
    meta: { requiresAuth: true, role: 'customer' }
  },
  // 店员相关路由
  {
    path: '/staff/order',
    name: 'StaffOrder',
    component: StaffOrder,
    meta: { requiresAuth: true, role: 'staff' }
  },
  {
    path: '/staff/product',
    name: 'StaffProduct',
    component: StaffProduct,
    meta: { requiresAuth: true, role: 'staff' }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：检查用户登录状态和权限
router.beforeEach((to, from, next) => {
  // 获取本地存储的token和角色
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  
  // 检查目标路由是否需要认证
  if (to.meta.requiresAuth) {
    // 如果没有token，表示未登录，跳转到登录页
    if (!token) {
      next('/')
      return
    }
    
    // 如果路由指定了角色要求，检查用户角色是否匹配
    if (to.meta.role && to.meta.role !== role) {
      // 角色不匹配，根据用户角色跳转到对应首页
      next(role === 'customer' ? '/menu' : '/staff/order')
      return
    }
  }
  
  // 允许访问
  next()
})

export default router