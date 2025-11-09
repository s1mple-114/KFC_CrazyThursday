// 购物车功能测试脚本
import { useCartStore } from '../store/cartstore'

// 模拟Vue组件环境
export function testCartFunctionality() {
  console.log('=== 购物车功能测试开始 ===')
  
  // 创建测试环境
  const mockApp = {}
  
  // 清除之前的测试数据
  localStorage.removeItem('cartList')
  console.log('已清除localStorage中的购物车数据')
  
  try {
    // 初始化购物车store
    const cartStore = useCartStore()
    console.log('购物车store初始化成功')
    
    // 测试初始状态
    console.log('初始购物车列表:', cartStore.cartList)
    console.log('初始购物车数量:', cartStore.totalCount)
    console.log('初始购物车金额:', cartStore.totalAmount)
    
    // 测试添加商品
    const testProduct = {
      id: 1,
      name: '测试商品',
      price: 10.00,
      category: 'DRINK'
    }
    
    console.log('\n添加商品:', testProduct)
    cartStore.addToCart(testProduct)
    console.log('添加后购物车列表:', cartStore.cartList)
    console.log('添加后购物车数量:', cartStore.totalCount)
    console.log('添加后购物车金额:', cartStore.totalAmount)
    
    // 测试再次添加同一商品（数量增加）
    console.log('\n再次添加同一商品')
    cartStore.addToCart(testProduct)
    console.log('再次添加后购物车列表:', cartStore.cartList)
    console.log('再次添加后购物车数量:', cartStore.totalCount)
    console.log('再次添加后购物车金额:', cartStore.totalAmount)
    
    // 测试localStorage同步
    const localStorageData = localStorage.getItem('cartList')
    console.log('\nlocalStorage中的购物车数据:', localStorageData)
    console.log('localStorage数据解析:', JSON.parse(localStorageData))
    
    // 测试更新数量
    console.log('\n更新商品数量(+1)')
    cartStore.updateQuantity(1, 1)
    console.log('更新后购物车列表:', cartStore.cartList)
    console.log('更新后购物车数量:', cartStore.totalCount)
    
    // 测试移除商品
    console.log('\n移除商品')
    cartStore.removeFromCart(1)
    console.log('移除后购物车列表:', cartStore.cartList)
    console.log('移除后购物车数量:', cartStore.totalCount)
    console.log('移除后购物车金额:', cartStore.totalAmount)
    
    console.log('\n=== 购物车功能测试完成 ===')
    return true
  } catch (error) {
    console.error('购物车功能测试失败:', error)
    console.log('=== 购物车功能测试失败 ===')
    return false
  }
}

// 如果直接运行此脚本
if (typeof window !== 'undefined') {
  testCartFunctionality()
}