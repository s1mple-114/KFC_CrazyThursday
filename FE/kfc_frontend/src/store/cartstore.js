import { defineStore } from 'pinia'

// 定义购物车状态
export const useCartStore = defineStore('cart', {
  // 状态：购物车列表（格式：[{id, name, price, quantity, category, status}, ...]）
  state: () => ({
    cartList: JSON.parse(localStorage.getItem('cartList')) || [] // 从本地存储读取，刷新页面不丢失
  }),

  // 方法：操作购物车的函数
  actions: {
    // 1. 添加商品到购物车
    addToCart(product) {
      // 检查商品是否已在购物车
      const existingItem = this.cartList.find(item => item.id === product.id)
      if (existingItem) {
        // 已存在：数量+1
        existingItem.quantity += 1
      } else {
        // 不存在：添加新商品（带数量1）
        this.cartList.push({ ...product, quantity: 1 })
      }
      // 同步到本地存储
      this.saveToLocalStorage()
    },

    // 2. 修改商品数量
    updateQuantity(productId, change) {
      const item = this.cartList.find(item => item.id === productId)
      if (item) {
        item.quantity += change
        // 数量不能小于1
        if (item.quantity < 1) item.quantity = 1
        this.saveToLocalStorage()
      }
    },

    // 3. 删除购物车商品
    removeFromCart(productId) {
      this.cartList = this.cartList.filter(item => item.id !== productId)
      this.saveToLocalStorage()
    },

    // 4. 清空购物车
    clearCart() {
      this.cartList = []
      this.saveToLocalStorage()
    },

    // 5. 同步到本地存储（私有方法）
    saveToLocalStorage() {
      localStorage.setItem('cartList', JSON.stringify(this.cartList))
    }
  },

  // 计算属性：获取购物车总金额、总数量等
  getters: {
    // 总金额
    totalAmount: (state) => {
      return state.cartList.reduce((total, item) => total + (item.price * item.quantity), 0)
    },
    // 总数量
    totalCount: (state) => {
      return state.cartList.reduce((total, item) => total + item.quantity, 0)
    }
  }
})