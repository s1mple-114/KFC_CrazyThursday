<template>
  <div class="menu-container">
    <!-- 引入导航栏组件 -->
    <Navbar />

    <!-- 分类导航 -->
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

    <!-- 商品列表（加载中状态） -->
    <el-skeleton v-if="loading" row-count="6" :columns="3" style="margin-top: 20px" />

    <!-- 商品列表（加载完成） -->
    <div class="product-list" v-else>
      <!-- 无商品时提示 -->
      <div class="no-product" v-if="filteredProducts.length === 0">
        <p>暂无该分类商品～</p>
      </div>
      <!-- 商品卡片 -->
      <el-card 
        v-for="product in filteredProducts" 
        :key="product.id"
        class="product-card"
        shadow="hover"
      >
        <!-- 商品图片（用占位图，实际项目替换为后端返回的图片地址） -->
        <img 
          :src="product.imgUrl || 'https://picsum.photos/300/200'" 
          alt="商品图片" 
          class="product-img"
        >
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-bottom">
            <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
            <!-- 上架商品显示"加入购物车"，下架显示"已下架" -->
            <el-button 
              type="primary" 
              size="small"
              @click="addToCart(product)"
              v-if="product.status === '上架'"
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

// 1. 购物车状态
const cartStore = useCartStore()
// 2. 加载状态（商品未加载完时显示骨架屏）
const loading = ref(true)
// 3. 所有分类（和后端商品分类对应）
const categories = ref(['全部', '汉堡', '炸鸡', '饮品', '甜点'])
// 4. 当前激活的分类
const activeCategory = ref('全部')
// 5. 后端返回的所有商品列表
const allProducts = ref([])

// 6. 筛选当前分类的商品（计算属性）
const filteredProducts = computed(() => {
  if (activeCategory.value === '全部') {
    return allProducts.value
  }
  return allProducts.value.filter(product => product.category === activeCategory.value)
})

// 7. 从后端获取商品列表
const getProductList = async () => {
  try {
    loading.value = true
    // 调用后端商品列表接口（假设地址是/product）
    const res = await request.get('/product')
    allProducts.value = res.data // 后端返回的商品列表，格式需包含id/name/price/category/status/imgUrl
  } catch (error) {
    // 错误已被request拦截器处理，这里不用额外操作
  } finally {
    loading.value = false
  }
}

// 8. 添加商品到购物车
const addToCart = (product) => {
  cartStore.addToCart(product)
  ElMessage.success(`已添加${product.name}到购物车～`)
}

// 9. 页面加载时获取商品数据
onMounted(() => {
  getProductList()
})
</script>

<style scoped>
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
  margin-bottom: 10px;
  flex: 1;
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