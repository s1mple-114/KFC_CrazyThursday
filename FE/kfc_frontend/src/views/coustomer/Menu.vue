<template>
  <div class="menu-container">
    <Navbar />
    <div class="category-tabs">
      <el-button 
        v-for="(category, index) in categories" 
        :key="index"
        :class="activeCategory === category ? 'active' : ''"
        @click="activeCategory = category"
        size="medium"
      >
        {{ category }}
      </el-button>
    </div>
    <el-skeleton v-if="loading" row-count="6" :columns="3" style="margin-top: 20px" />
    <div class="product-list" v-else>
      <div class="no-product" v-if="filteredProducts.length === 0">
        <p>暂无该分类商品～</p>
        <p style="font-size: 12px; color: #999;">
          调试：当前分类{{ activeCategory }}，匹配标识{{ categoryMap[activeCategory] }}，总商品数{{ allProducts.length }}
        </p>
      </div>
      <el-card 
        v-for="product in filteredProducts" 
        :key="product.id"  
        class="product-card"
        shadow="hover"
      >
        <img 
          :src="product.image || 'https://picsum.photos/300/200'" 
          alt="商品图片" 
          class="product-img"
        >
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-desc">{{ product.description }}</p>
          <div class="product-bottom">
            <span class="product-price">¥{{ product.price }}</span>
            <el-button 
              type="primary" 
              size="small"
              @click="addToCart(product)"
              v-if="product.is_available"
            >
              加入购物车
            </el-button>
            <el-button 
              size="small"
              disabled
              v-else
            >
              已下架
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import Navbar from '../../components/Navbar.vue'
import request from '../../utils/request'
import { useCartStore } from '../../store/cartStore'

// 1. 分类映射严格匹配后端实际返回值（汉堡为"BURGER"单数）
const categoryMap = {
  '全部': '',
  '汉堡': 'BURGER',  // 匹配数据中的"BURGER"
  '炸鸡': 'FOOD',
  '饮品': 'DRINK',   // 匹配数据中的"DRINK"
  '甜点': 'DESSERT'
}

// 2. 筛选逻辑
const filteredProducts = computed(() => {
  const currentCategory = categoryMap[activeCategory.value]
  console.log('筛选调试：', {
    前端分类: activeCategory.value,
    后端匹配值: currentCategory,
    商品总数: allProducts.value.length,
    所有商品分类: allProducts.value.map(item => item.category)
  })

  if (!currentCategory) {
    return allProducts.value
  }
  return allProducts.value.filter(product => product.category === currentCategory)
})

// 3. 状态定义
const cartStore = useCartStore()
const loading = ref(true)
const categories = ref(['全部', '汉堡', '炸鸡', '饮品', '甜点'])
const activeCategory = ref('全部')
const allProducts = ref([])

// 4. 获取商品列表（适配对象+数组结构）
const getProductList = async () => {
  try {
    loading.value = true
    console.log('开始请求接口...')
    
    // 使用相对路径，因为request.js已设置baseURL为'/api'
    const res = await request.get('/products/products/')
    
    // 打印响应确认结构 - 详细调试
    console.log('=== 响应调试信息 ===')
    console.log('响应对象类型:', typeof res)
    console.log('是否为数组:', Array.isArray(res))
    console.log('响应对象结构:', res)
    console.log('响应对象长度:', res ? Object.keys(res).length : 'undefined')
    
    // 健壮的响应处理
    let productsArray = []
    
    // 处理不同可能的响应格式
    if (Array.isArray(res)) {
      // 如果直接是数组
      productsArray = res
      console.log('直接获取到数组，长度:', res.length)
    } else if (res && Array.isArray(res.results)) {
      // 如果是包含results数组的对象
      productsArray = res.results
      console.log('从results字段获取数组，长度:', res.results.length)
    } else if (res && typeof res === 'object') {
      // 尝试其他可能的字段
      console.log('响应是对象，尝试查找数据数组...')
      console.log('对象键:', Object.keys(res))
      
      // 如果对象只有一个数组类型的键，可能就是数据
      for (const key in res) {
        if (Array.isArray(res[key])) {
          productsArray = res[key]
          console.log(`从${key}字段获取数组，长度:`, res[key].length)
          break
        }
      }
    }
    
    // 验证是否获取到了数据
    if (productsArray.length === 0) {
      console.warn('未找到商品数据，响应可能不是预期格式')
      // 不抛出错误，而是显示空数据
      allProducts.value = []
    } else {
      console.log('成功获取商品数据，开始处理...')
      allProducts.value = productsArray.map((item) => ({
  id: item.id,
  name: item.name || '未知商品',
  price: item.price || '0.00',
  category: item.category || '未知分类',
  description: item.description || '无描述',
  image: item.image,
  is_available: item.is_available !== undefined ? item.is_available : false
}))
    
    console.log('解析成功，商品数量：', allProducts.value.length)
    ElMessage.success(`加载成功，共${allProducts.value.length}件商品`)

  } catch (error) {
    console.error('获取商品失败：', error.message)
    ElMessage.error(`加载失败：${error.message}`)
  } finally {
    loading.value = false
  }
}

// 5. 添加购物车逻辑
const addToCart = (product) => {
  const productWithNumberPrice = {
    ...product,
    price: Number(product.price)
  }
  cartStore.addToCart(productWithNumberPrice)
  ElMessage.success(`已添加${product.name}到购物车～`)
}

// 6. 页面加载时请求数据
onMounted(() => {
  getProductList()
})
</script>

<style scoped>
/* 样式部分保持不变 */
.menu-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
.category-tabs {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.category-tabs .el-button {
  border-color: #D32F2F;
  color: #D32F2F;
}
.category-tabs .el-button.active {
  background-color: #D32F2F;
  color: #fff;
}
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.product-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.product-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px 4px 0 0;
}
.product-info {
  padding: 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.product-name {
  font-size: 16px;
  margin-bottom: 5px;
  flex: none;
}
.product-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp:2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.product-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}
.product-price {
  font-size: 16px;
  color: #D32F2F;
  font-weight: bold;
}
.no-product {
  text-align: center;
  padding: 50px;
  color: #999;
}
</style>