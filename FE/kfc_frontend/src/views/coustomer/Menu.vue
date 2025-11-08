<template>
  <div class="menu-container">
   <!-- 暂时移除Navbar组件，使用简单标题替代 -->
    <div class="navbar-simple">
      <h1>KFC订单系统</h1>
    </div>
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
            >
              加入购物车
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
// 暂时移除Navbar组件，避免加载错误
// import Navbar from '../../components/Navbar.vue'
// 移除未使用的request导入
import { useCartStore } from '../../store/cartStore'

const categoryMap = {
  '全部': '',
  '汉堡': 'BURGER',  // 匹配后端BURGER
  '小食': 'SNACK',   // 匹配后端SNACK
  '饮料': 'DRINK',   // 匹配后端DRINK，与后端保持一致
  '套餐': 'COMBO'    // 匹配后端COMBO
}

// 2. 筛选逻辑（保持不变）
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

// 3. 状态定义（更新分类选项）
const cartStore = useCartStore()
const loading = ref(false) // 直接设置为false，不加载
// 分类选项与后端保持一致
const categories = ref(['全部', '汉堡', '小食', '饮料', '套餐'])
const activeCategory = ref('全部')
// 直接初始化商品数据，不等待API
const allProducts = ref([
  {
    id: 1,
    name: '可乐',
    price: 10.00,
    category: 'DRINK',
    description: '冰爽可乐',
    image: null
  },
  {
    id: 2,
    name: '超级无敌大汉堡',
    price: 100.00,
    category: 'BURGER',
    description: '超级好吃',
    image: null
  }
])

// 4. 获取商品列表（保持不变）
// 简化版：直接使用硬编码数据，不调用API
const getProductList = () => {
  console.log('使用硬编码商品数据');
  console.log('商品数据:', allProducts.value);
  console.log('商品总数:', allProducts.value.length);
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

// 6. 页面加载时初始化数据（实际上数据已经在定义时初始化了）
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

/* 简单的标题栏样式 */
.navbar-simple {
  background-color: #D32F2F;
  color: white;
  padding: 15px 20px;
  margin-bottom: 20px;
  text-align: center;
}

.navbar-simple h1 {
  margin: 0;
  font-size: 24px;
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