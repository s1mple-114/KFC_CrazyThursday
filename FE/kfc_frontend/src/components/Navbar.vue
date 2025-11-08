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

    <!-- 右侧：购物车（顾客可见）+ 退出登录 -->
    <el-menu-item index="3" style="margin-left: auto" v-if="userRole === 'customer'" @click="showCart">
      <i class="el-icon-shopping-cart" style="margin-right: 5px"></i>      
      <span>购物车</span>
      <!-- 购物车商品数量角标 -->
      <el-badge :value="cartCount" class="badge" v-if="cartCount > 0"></el-badge>
    </el-menu-item>

    <el-menu-item index="4" style="margin-left: 10px" @click="handleLogout">
      <i class="el-icon-switch-button" style="margin-right: 5px"></i>
      <span>退出登录</span>
    </el-menu-item>
  </el-menu>

  <!-- 顾客购物车抽屉（点击购物车显示） -->
  <el-drawer 
    title="我的购物车" 
    :visible="cartVisible" 
    direction="rtl"
    @close="cartVisible = false"
    v-if="userRole === 'customer'"
  >
    <!-- 购物车为空 -->
    <div class="cart-empty" v-if="cartCount === 0">
      <i class="el-icon-shopping-cart-empty" style="font-size: 40px; color: #ccc"></i>
      <p style="margin-top: 10px; color: #999">购物车是空的，快去选商品吧～</p>
    </div>
    <!-- 购物车有商品 -->
    <div class="cart-has-item" v-else>
      <!-- 商品列表 -->
      <div class="cart-items">
        <div 
          v-for="item in cartStore.cartList" 
          :key="item.id" 
          class="cart-item"
        >
          <!-- 商品信息 -->
          <div class="item-info">
            <div class="item-name">{{ item.name }}</div>
            <div class="item-price">¥{{ item.price.toFixed(2) }}</div>
          </div>
          
          <!-- 数量控制 -->
          <div class="item-quantity">
            <el-button 
              size="mini" 
              @click="cartStore.updateQuantity(item.id, -1)"
              :disabled="item.quantity <= 1"
            >
              -1
            </el-button>
            <span class="quantity-text">{{ item.quantity }}</span>
            <el-button 
              size="mini" 
              @click="cartStore.updateQuantity(item.id, 1)"
            >
              +1
            </el-button>
          </div>
          
          <!-- 删除按钮 -->
          <el-button 
            size="mini" 
            type="danger" 
            @click="cartStore.removeFromCart(item.id)"
          >
            删除
          </el-button>
        </div>
      </div>
      
      <!-- 底部结算信息 -->
      <div class="cart-footer">
        <div class="total-info">
          <span>总计：</span>
          <span class="total-price">¥{{ cartStore.totalAmount }}</span>
        </div>
        <el-button type="primary" @click="goToCheckout" :disabled="cartStore.totalCount === 0">
          去结算
        </el-button>
      </div>
    </div>
  </el-drawer>
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
// 3. 购物车抽屉显示状态
const cartVisible = ref(false)
// 4. 购物车状态（后续创建cartStore后生效）
const cartStore = useCartStore()
// 5. 购物车商品数量（计算属性）
const cartCount = computed(() => {
  return cartStore.cartList.reduce((total, item) => total + item.quantity, 0)
})

// 6. 显示购物车抽屉
const showCart = () => {
  cartVisible.value = true
}

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

// 9. 去结算（跳订单提交页）
const goToCheckout = () => {
  router.push('/order-submit')
  cartVisible.value = false
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