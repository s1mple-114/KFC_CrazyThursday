<template>
  <div class="cart-container">
    <div class="cart-header">
      <h2>我的购物车</h2>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><a href="/menu">菜单</a></el-breadcrumb-item>
        <el-breadcrumb-item>购物车</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    
    <!-- 购物车为空 -->
    <div class="cart-empty" v-if="cartStore.totalCount === 0">
      <el-empty
        description="购物车还是空的，快去添加商品吧！"
      >
        <el-button type="primary" @click="goToMenu">去逛逛</el-button>
      </el-empty>
    </div>
    
    <!-- 购物车有商品 -->
    <div class="cart-content" v-else>
      <!-- 商品列表 -->
      <el-table :data="cartStore.cartList" style="width: 100%" class="cart-table">
        <el-table-column width="55" align="center">
          <template #default="scope">
            <el-checkbox :checked="scope.row.isChecked" @change="handleItemCheck(scope.row.id)">
            </el-checkbox>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="商品名称" min-width="200">
          <template #default="scope">
            <div class="product-info">
              <div class="product-name">{{ scope.row.name }}</div>
              <div class="product-category" v-if="scope.row.category">
                {{ getCategoryText(scope.row.category) }}
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="price" label="单价" width="120" align="center">
          <template #default="scope">
            <span class="price">¥{{ scope.row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="quantity" label="数量" width="180" align="center">
          <template #default="scope">
            <div class="quantity-control">
              <el-button
                size="small"
                @click="decreaseQuantity(scope.row.id)"
                :disabled="scope.row.quantity <= 1"
              >
                -1
              </el-button>
              <span class="quantity-text">{{ scope.row.quantity }}</span>
              <el-button
                size="small"
                @click="increaseQuantity(scope.row.id)"
              >
                +1
              </el-button>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="小计" width="120" align="center">
          <template #default="scope">
            <span class="subtotal">¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="100" align="center">
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              @click="removeItem(scope.row.id, scope.row.name)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 底部操作栏 -->
      <div class="cart-footer">
        <div class="left-actions">
          <el-checkbox :checked="cartStore.isAllChecked" @change="handleAllCheck">
            全选
          </el-checkbox>
          <el-button type="danger" size="small" @click="clearCart" :disabled="cartStore.totalCount === 0">
            清空购物车
          </el-button>
        </div>
        
        <div class="right-actions">
          <div class="total-info">
            <span>已选商品：{{ cartStore.checkedCount }} 件</span>
            <span class="total-price">
              合计：¥{{ cartStore.totalAmount }}
            </span>
          </div>
          <el-button type="primary" @click="goToCheckout" :disabled="cartStore.checkedCount === 0">
            去结算
            <el-badge :value="cartStore.checkedCount" class="checkout-badge" v-if="cartStore.checkedCount > 0"></el-badge>
          </el-button>
        </div>
      </div>
      

    </div>
  </div>
</template>

<script>
import { useCartStore } from '../../store/cartstore'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

export default {
  name: 'Cart',
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    // 获取分类文本
    const getCategoryText = (category) => {
      const categoryMap = {
        'BURGER': '汉堡',
        'SNACK': '小食',
        'DRINK': '饮料',
        'COMBO': '套餐',
        'burger': '汉堡',
        'snack': '小吃',
        'drink': '饮料',
        'combo': '套餐'
      }
      return categoryMap[category] || category
    }
    
    // 处理单个商品勾选
    const handleItemCheck = (productId) => {
      cartStore.toggleCheck(productId)
    }
    
    // 处理全选
    const handleAllCheck = () => {
      cartStore.toggleAllCheck()
    }
    
    // 减少商品数量
    const decreaseQuantity = (productId) => {
      cartStore.updateQuantity(productId, -1)
    }
    
    // 增加商品数量
    const increaseQuantity = (productId) => {
      cartStore.updateQuantity(productId, 1)
    }
    
    // 删除单个商品
    const removeItem = (productId, productName) => {
      cartStore.removeFromCart(productId)
      ElMessage.success(`商品「${productName}」已从购物车中删除`)
    }
    
    // 清空购物车
    const clearCart = () => {
      cartStore.clearCart()
      ElMessage.success('购物车已清空')
    }
    
    // 去菜单页面
    const goToMenu = () => {
      router.push('/menu')
    }
    
    // 去结算页面
    const goToCheckout = () => {
      const checkedItems = cartStore.checkedGoods
      if (checkedItems.length === 0) {
        ElMessage.warning('请选择要结算的商品')
        return
      }
      
      // 跳转到结算页面
      router.push('/order-submit')
    }
    

    
    return {
      cartStore,
      getCategoryText,
      handleItemCheck,
      handleAllCheck,
      decreaseQuantity,
      increaseQuantity,
      removeItem,
      clearCart,
      goToMenu,
      goToCheckout
    }
  }
}
</script>

<style scoped>
.cart-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.cart-header {
  margin-bottom: 20px;
}

.cart-header h2 {
  margin-bottom: 10px;
  color: #303133;
}

.cart-empty {
  background-color: #fff;
  padding: 60px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cart-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cart-table {
  margin-bottom: 20px;
}

.product-info {
  line-height: 1.5;
}

.product-name {
  font-weight: 500;
  margin-bottom: 5px;
}

.product-category {
  color: #909399;
  font-size: 12px;
}

.price {
  color: #D32F2F;
  font-weight: bold;
}

.subtotal {
  color: #D32F2F;
  font-weight: bold;
  font-size: 16px;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity-text {
  min-width: 30px;
  text-align: center;
}

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-top: 1px solid #eee;
  margin-top: 20px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.right-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.total-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

.total-price {
  font-size: 20px;
  color: #D32F2F;
  font-weight: bold;
}

.checkout-badge {
  margin-left: 5px;
}


</style>