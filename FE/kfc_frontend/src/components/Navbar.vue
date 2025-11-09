<template>
  <el-menu 
    mode="horizontal" 
    background-color="#D32F2F" 
    text-color="#fff" 
    active-text-color="#fff"
    class="navbar"
  >
    <!-- 左侧Logo/标题 -->
    <el-menu-item index="1">
      <i class="el-icon-shopping-bag" style="margin-right: 5px"></i>
      <span>KFC订单系统</span>
    </el-menu-item>

    <!-- 中间：店员端导航（只有店员可见） -->
    <el-sub-menu index="2" v-if="userRole === 'staff'">
      <template #title>管理中心</template>
      <el-menu-item index="2-1" @click="goToPage('/staff/order')">订单管理</el-menu-item>
      <el-menu-item index="2-2" @click="goToPage('/staff/product')">商品管理</el-menu-item>
    </el-sub-menu>

    <!-- 右侧：我的订单、购物车（顾客可见）+ 退出登录 -->
    <el-menu-item index="3" style="margin-left: auto" v-if="userRole === 'customer'">
      <router-link to="/order-list" style="display: flex; align-items: center; color: inherit;">
        <i class="el-icon-document" style="margin-right: 5px"></i>      
        <span>我的订单</span>
      </router-link>
    </el-menu-item>
    
    <el-menu-item index="4" style="margin-left: 10px" v-if="userRole === 'customer'">
      <router-link to="/cart" style="display: flex; align-items: center; color: inherit;">
        <i class="el-icon-shopping-cart" style="margin-right: 5px"></i>      
        <span>购物车</span>
        <!-- 购物车商品数量角标 -->
        <el-badge :value="cartCount" class="badge" v-if="cartCount > 0"></el-badge>
      </router-link>
    </el-menu-item>

    <el-menu-item index="5" style="margin-left: 10px" @click="handleLogout">
      <i class="el-icon-switch-button" style="margin-right: 5px"></i>
      <span>退出登录</span>
    </el-menu-item>
  </el-menu>

  <!-- 购物车功能已转移到独立页面 /cart -->
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCartStore } from '../store/cartStore' // 后续创建的购物车状态

// 1. 路由实例
const router = useRouter()
// 2. 当前用户角色（从本地存储获取）
const userRole = ref(localStorage.getItem('role') || '')
// 4. 购物车状态（后续创建cartStore后生效）
const cartStore = useCartStore()
// 5. 购物车商品数量（计算属性）
const cartCount = computed(() => {
  return cartStore.cartList.reduce((total, item) => total + item.quantity, 0)
})

// 7. 退出登录
const handleLogout = () => {
  // 清除本地存储的Token和角色
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  // 清空购物车（如果是顾客）
  if (userRole.value === 'customer') {
    cartStore.clearCart()
  }
  // 跳登录页
  router.push('/login')
  ElMessage.success('已退出登录')
}

// 8. 跳转到指定页面
const goToPage = (path) => {
  router.push(path)
}
</script>

<style scoped>
.navbar {
  margin-bottom: 20px;
}
.badge {
  position: absolute;
  top: 10px;
  right: 10px;
}
.cart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

/* 购物车样式 */
.cart-has-item {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 购物车商品列表 */
.cart-items {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-bottom: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  gap: 15px;
}

/* 商品信息 */
.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-weight: 500;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-price {
  color: #D32F2F;
  font-weight: bold;
}

/* 数量控制 */
.item-quantity {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 120px;
}

.quantity-text {
  min-width: 30px;
  text-align: center;
}

/* 底部结算信息 */
.cart-footer {
  padding: 20px 15px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fafafa;
  margin: 0 -20px -20px;
}

.total-info {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.total-price {
  font-size: 20px;
  color: #D32F2F;
  font-weight: bold;
}
</style>