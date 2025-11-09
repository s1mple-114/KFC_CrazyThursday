<template>
  <!-- 导航栏组件：使用Element Plus的水平菜单 -->
  <!-- 配置项说明：
    - mode="horizontal"：水平布局
    - background-color="#D32F2F"：红色背景（KFC品牌色）
    - text-color="#fff"：默认文字白色
    - active-text-color="#fff"：激活状态文字白色
  -->
  <el-menu mode="horizontal" background-color="#D32F2F" text-color="#fff" active-text-color="#fff" class="navbar">
    <!-- 左侧Logo/标题区域 -->
    <el-menu-item index="1">
      <i class="el-icon-shopping-bag"></i> <!-- 购物袋图标 -->
      <span>KFC订单系统</span> <!-- 系统标题 -->
    </el-menu-item>

    <!-- 右侧功能区 -->
    <!-- 购物车按钮：仅顾客角色可见 -->
    <el-menu-item 
      index="3" 
      style="margin-left: auto"  <!-- 自动右对齐 -->
      v-if="userRole === 'customer'"  <!-- 权限控制：仅顾客显示 -->
      @click="showCart"  <!-- 点击打开购物车抽屉 -->
    >
      <i class="el-icon-shopping-cart"></i> <!-- 购物车图标 -->
      <span>购物车 ({{ cartCount }})</span> <!-- 显示购物车商品总数 -->
    </el-menu-item>

    <!-- 退出登录按钮：所有角色可见 -->
    <el-menu-item 
      index="4" 
      style="margin-left: 10px"  <!-- 与左侧元素保持间距 -->
      @click="handleLogout"  <!-- 点击触发退出登录逻辑 -->
    >
      <i class="el-icon-switch-button"></i> <!-- 切换图标 -->
      <span>退出登录</span>
    </el-menu-item>
  </el-menu>

  <!-- 购物车抽屉组件：从右侧滑出 -->
  <el-drawer 
    title="我的购物车"  <!-- 抽屉标题 -->
    :visible="cartVisible"  <!-- 控制抽屉显示/隐藏的变量 -->
    direction="rtl"  <!-- 从右侧滑出 -->
    @close="cartVisible = false"  <!-- 关闭抽屉时的回调 -->
    v-if="userRole === 'customer'"  <!-- 权限控制：仅顾客显示 -->
  >
    <!-- 购物车为空时的提示 -->
    <div v-if="cartStore.cartList.length === 0">
      <p>购物车为空</p>
    </div>
    <!-- 购物车有商品时的列表 -->
    <div v-else>
      <!-- 遍历购物车列表，渲染每个商品项 -->
      <div v-for="item in cartStore.cartList" :key="item.id" class="cart-item">
        <div>{{ item.name }} - ¥{{ item.price }}</div>  <!-- 商品名称和单价 -->
        <div>数量: {{ item.quantity }}</div>  <!-- 商品数量 -->
        <!-- 数量操作按钮组 -->
        <el-button size="mini" @click="cartStore.updateQuantity(item.id, 1)">+</el-button>  <!-- 增加数量 -->
        <el-button size="mini" @click="cartStore.updateQuantity(item.id, -1)">-</el-button>  <!-- 减少数量 -->
        <el-button size="mini" type="danger" @click="cartStore.removeFromCart(item.id)">删除</el-button>  <!-- 从购物车移除 -->
      </div>
      <!-- 显示购物车商品总价 -->
      <div style="margin-top: 20px">总计: ¥{{ cartStore.totalAmount }}</div>
    </div>
  </el-drawer>
</template>

<script setup>
// 导入Vue核心API
import { ref, computed, onMounted } from 'vue'
// 导入路由工具
import { useRouter } from 'vue-router'
// 导入Element Plus消息提示组件
import { ElMessage } from 'element-plus'
// 导入购物车状态管理模块
import { useCartStore } from '../store/cartstore'

// 路由实例，用于页面跳转
const router = useRouter()
// 用户角色：从本地存储获取，默认为空（未登录状态）
const userRole = ref(localStorage.getItem('role') || '')
// 控制购物车抽屉显示/隐藏的状态变量
const cartVisible = ref(false)
// 获取购物车状态管理实例
const cartStore = useCartStore()

// 计算属性：计算购物车商品总数量（累加所有商品的数量）
const cartCount = computed(() => {
  return cartStore.cartList.reduce((total, item) => total + item.quantity, 0)
})

// 打开购物车抽屉的方法
const showCart = () => {
  cartVisible.value = true
  console.log('购物车内容:', cartStore.cartList)  // 调试用：打印购物车数据
}

// 处理退出登录的方法
const handleLogout = () => {
  // 清除本地存储中的登录凭证和角色信息
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  // 如果是顾客角色，退出时清空购物车
  if (userRole.value === 'customer') {
    cartStore.clearCart()
  }
  // 跳转到登录页面
  router.push('/login')
}

// 组件挂载完成后执行的逻辑
onMounted(() => {
  // 延迟1秒执行（确保状态初始化完成）
  setTimeout(() => {
    console.log('初始购物车状态:', cartStore.cartList)  // 调试用：打印初始购物车状态
    // 开发环境下，如果购物车为空，添加测试商品（方便开发调试）
    if (import.meta.env.DEV && cartStore.cartList.length === 0) {
      const testProduct = { id: 999, name: '测试可乐', price: 10.00, category: 'DRINK' }
      cartStore.addToCart(testProduct)  // 调用购物车方法添加商品
      ElMessage.success('已添加测试商品')  // 显示成功提示
    }
  }, 1000)
})
</script>

<style scoped>
/* 导航栏样式：底部外边距 */
.navbar { margin-bottom: 20px; }
/* 购物车商品项样式：底部间距、内边距和边框 */
.cart-item { margin-bottom: 10px; padding: 10px; border: 1px solid #eee; }
</style>