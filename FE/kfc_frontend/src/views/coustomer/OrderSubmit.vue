<template>
  <div class="order-submit-container">
    <div class="order-header">
      <h2>订单确认</h2>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><a href="/menu">菜单</a></el-breadcrumb-item>
        <el-breadcrumb-item><a href="/cart">购物车</a></el-breadcrumb-item>
        <el-breadcrumb-item>订单确认</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 无商品时的提示 -->
    <div class="empty-tip" v-if="cartStore.checkedGoods.length === 0">
      <el-empty description="请选择要结算的商品">
        <el-button type="primary" @click="goToCart">返回购物车</el-button>
      </el-empty>
    </div>

    <!-- 有商品时的结算信息 -->
    <div class="order-content" v-else>

      <!-- 商品清单 -->
      <div class="goods-section">
        <h3>商品清单</h3>
        <el-table :data="cartStore.checkedGoods" style="width: 100%" class="order-table">
          <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
          <el-table-column prop="price" label="单价" width="120" align="center">
            <template #default="scope">
              ¥{{ scope.row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
          <el-table-column label="小计" width="120" align="center">
            <template #default="scope">
              ¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 订单备注 -->
      <div class="remark-section">
        <h3>订单备注</h3>
        <el-input v-model="remark" placeholder="如有特殊要求，请在此备注" :rows="3" type="textarea"></el-input>
      </div>

      <!-- 订单金额 -->
      <div class="summary-section">
        <div class="summary-item">
          <span>商品总价</span>
          <span class="price">¥{{ cartStore.totalAmount }}</span>
        </div>
        <div class="summary-item">
          <span>配送费</span>
          <span class="price">¥0.00</span>
        </div>
        <div class="summary-item total">
          <span>实付款</span>
          <span class="total-price">¥{{ cartStore.totalAmount }}</span>
        </div>
      </div>

      <!-- 提交订单按钮 -->
      <div class="submit-section">
        <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
          提交订单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '../../store/cartstore'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'
import { reactive, ref } from 'vue'

export default {
  name: 'OrderSubmit',
  setup() {
    const cartStore = useCartStore()
    const router = useRouter()
    const submitting = ref(false)
    const remark = ref('')
    
    // 返回购物车
    const goToCart = () => {
      router.push('/cart')
    }
    
    // 提交订单
    const submitOrder = async () => {
      submitting.value = true
      
      try {
        // 构建订单数据
        const orderData = {
          items: cartStore.checkedGoods.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price
          })),
          total_amount: parseFloat(cartStore.totalAmount),
          remark: remark.value
        }
        
        // 发送请求到后端创建订单
        const response = await request.post('/api/orders/orders/', orderData)
        
        // 清除购物车中已结算的商品
        cartStore.checkedGoods.forEach(item => {
          cartStore.removeFromCart(item.id)
        })
        
        // 获取订单ID
        const orderId = response.data.id || response.data.order_number
        const totalAmount = cartStore.totalAmount
        
        // 保存金额到本地存储，以便支付页面使用
        localStorage.setItem('payment_amount', totalAmount)
        
        // 跳转到支付页面
        router.push({
          path: '/payment',
          query: { order_id: orderId }
        })
      } catch (error) {
        console.error('提交订单失败:', error)
        ElMessage.error('订单提交失败，请稍后重试')
      } finally {
        submitting.value = false
      }
    }
    
    return {
      cartStore,
      router,
      remark,
      submitting,
      goToCart,
      submitOrder
    }
  }
}
</script>

<style scoped>
.order-submit-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.order-header {
  margin-bottom: 20px;
}

.order-header h2 {
  margin-bottom: 10px;
  color: #303133;
}

.empty-tip {
  background-color: #fff;
  padding: 60px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.goods-section,
.remark-section,
.summary-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

h3 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.order-table {
  margin-bottom: 10px;
}

.price {
  color: #606266;
}

.total-price {
  color: #D32F2F;
  font-size: 20px;
  font-weight: bold;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.summary-item.total {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
}

.submit-section {
  text-align: right;
  padding-top: 20px;
}
</style>