import { defineStore } from 'pinia'

// 定义并导出购物车Store，命名为"cart"（全局唯一）
export const useCartStore = defineStore('cart', {
  // 1. 状态：存储购物车核心数据（刷新页面不丢失）
  state: () => ({
    // 购物车列表：数组格式，每个元素是商品对象
    cartList: JSON.parse(localStorage.getItem('cartList')) || [], 
    // 可选：是否勾选全选（后续结算页用）
    isAllChecked: false
  }),

  // 2. 操作方法：修改购物车数据的函数（增删改查）
  actions: {
    // ① 添加商品到购物车（已存在则数量+1，不存在则新增）
    addToCart(product) {
      const existingItem = this.cartList.find(item => item.id === product.id)
      if (existingItem) {
        existingItem.quantity += 1 // 已存在：数量+1
      } else {
        // 不存在：新增商品（需包含核心字段，其他字段按需加）
        this.cartList.push({
          id: product.id,       // 商品唯一ID（必传）
          name: product.name,   // 商品名称（必传）
          price: product.price, // 商品单价（必传）
          imgUrl: product.imgUrl, // 商品图片（可选）
          category: product.category, // 商品分类（可选）
          status: product.status, // 商品状态（可选）
          quantity: 1,          // 初始数量（必传）
          isChecked: true       // 是否勾选（结算用，必传）
        })
      }
      this.saveToLocalStorage() // 同步到本地存储，刷新不丢数据
    },

    // ② 修改商品数量（+1/-1）
    updateQuantity(productId, change) {
      const item = this.cartList.find(item => item.id === productId)
      if (item) {
        item.quantity += change
        item.quantity = Math.max(1, item.quantity) // 数量最小为1
        this.saveToLocalStorage()
      }
    },

    // ③ 单个商品勾选/取消勾选
    toggleCheck(productId) {
      const item = this.cartList.find(item => item.id === productId)
      if (item) {
        item.isChecked = !item.isChecked
        // 同步全选状态（所有商品勾选则全选勾选）
        this.isAllChecked = this.cartList.every(item => item.isChecked)
        this.saveToLocalStorage()
      }
    },

    // ④ 全选/取消全选
    toggleAllCheck() {
      this.isAllChecked = !this.isAllChecked
      this.cartList.forEach(item => item.isChecked = this.isAllChecked)
      this.saveToLocalStorage()
    },

    // ⑤ 删除购物车单个商品
    removeFromCart(productId) {
      this.cartList = this.cartList.filter(item => item.id !== productId)
      // 删除后检查是否需要更新全选状态
      this.isAllChecked = this.cartList.length > 0 && this.cartList.every(item => item.isChecked)
      this.saveToLocalStorage()
    },

    // ⑥ 清空购物车（退出登录/下单成功后用）
    clearCart() {
      this.cartList = []
      this.isAllChecked = false
      this.saveToLocalStorage()
    },

    // ⑦ 私有方法：同步数据到本地存储（内部调用，无需暴露）
    saveToLocalStorage() {
      localStorage.setItem('cartList', JSON.stringify(this.cartList))
    }
  },

  // 3. 计算属性：派生数据（无需手动更新，自动响应状态变化）
  getters: {
    // ① 购物车商品总数量
    totalCount: (state) => {
      return state.cartList.reduce((total, item) => total + item.quantity, 0)
    },

    // ② 购物车商品总金额（只计算勾选的商品）
    totalAmount: (state) => {
      return state.cartList
        .filter(item => item.isChecked)
        .reduce((total, item) => total + (item.price * item.quantity), 0)
        .toFixed(2) // 保留2位小数（金额格式）
    },

    // ③ 勾选的商品列表（结算时传给后端）
    checkedGoods: (state) => {
      return state.cartList.filter(item => item.isChecked)
    },
    
    // ④ 勾选的商品数量
    checkedCount: (state) => {
      return state.cartList
        .filter(item => item.isChecked)
        .reduce((total, item) => total + item.quantity, 0)
    }
  }
})