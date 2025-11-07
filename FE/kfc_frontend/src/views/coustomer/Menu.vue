<template>
  <div class="menu-container">
    <Navbar />
    <div class="category-tabs">
      <el-button 
        v-for="(category, index) in categories" 
        :key="index"
        :class="activeCategory === category ? 'active' : ''"
        @click="activeCategory = category"
        size="small"
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
  
  '饮品': 'DRINK',   // 匹配数据中的"DRINK"
  
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
// 在getProductList中赋值时，对商品字段做格式化：
const getProductList = async () => {
  try {
    loading.value = true
    const res = await request.get('/product')
    if (Array.isArray(res)) {
      // 对每个商品做字段格式化
      allProducts.value = res.map(item => ({
        id: item.id,
        name: item.name || '未知商品',
        price: Number(item.price) || 0.00, // 转数字
        category: item.category || '未知分类',
        description: item.description || '无描述',
        image: item.image,
        is_available: item.is_available !== undefined ? item.is_available : false, // 对应后端的is_available
        created_time: item.created_time
      }));
    } else {
      allProducts.value = [];
    }
  } catch (error) {
    allProducts.value = [];
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