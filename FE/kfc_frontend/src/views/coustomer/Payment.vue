<template>
  <div class="payment-container">
    <div class="payment-header">
      <h2>选择支付方式</h2>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><a href="/menu">菜单</a></el-breadcrumb-item>
        <el-breadcrumb-item><a href="/cart">购物车</a></el-breadcrumb-item>
        <el-breadcrumb-item><a href="/order-submit">订单确认</a></el-breadcrumb-item>
        <el-breadcrumb-item>支付</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="payment-content" v-if="orderId">
      <!-- 订单信息 -->
      <div class="order-info-section">
        <h3>订单信息</h3>
        <div class="order-info-item">
          <span>订单号：</span>
          <span>{{ orderId }}</span>
        </div>
        <div class="order-info-item">
          <span>支付金额：</span>
          <span class="amount">¥{{ totalAmount }}</span>
        </div>
      </div>

      <!-- 支付方式选择 -->
      <div class="payment-method-section">
        <h3>选择支付方式</h3>
        <el-radio-group v-model="selectedPayment" class="payment-options">
          <el-radio :label="'steam'" class="payment-option">
            <div class="payment-option-content">
              <div class="payment-icon steam-icon">
                <el-icon><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="48" height="48"><path d="M641.11 129.503L352.875 312.701v402.592l288.235 183.198v-585.69z" fill="#1b2838"/></svg></el-icon>
              </div>
              <div class="payment-text">
                <div class="payment-name">Steam钱包支付</div>
                <div class="payment-desc">使用Steam钱包余额进行支付</div>
              </div>
            </div>
          </el-radio>
          <el-radio :label="'wechat'" class="payment-option">
            <div class="payment-option-content">
              <div class="payment-icon wechat-icon">
                <el-icon><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="48" height="48"><path d="M896 0H128C57.312 0 0 57.312 0 128v768c0 70.688 57.312 128 128 128h768c70.688 0 128-57.312 128-128V128c0-70.688-57.312-128-128-128zM512 176c185.6 0 336 150.4 336 336s-150.4 336-336 336S176 697.6 176 522c0-180.352 140.8-327.104 315.648-335.36L512 176zm192.192 248.832c-8.96 35.584-31.872 65.6-61.12 83.712a160.128 160.128 0 0 1-105.152 32.832c-36.8 0-72.192-9.216-103.552-26.048-4.096-2.56-8.448-4.608-13.056-5.888-4.8-1.408-9.728-1.92-14.72-0.512-1.792 0.384-3.456 0.896-5.12 1.536-29.44 8.96-56.832 28.416-78.72 54.784-4.8 5.632-9.472 11.712-13.568 18.176-4.096 6.4-7.68 13.056-10.752 19.968-0.384 0.896-0.768 1.92-1.28 2.944a383.616 383.616 0 0 0-6.912 12.8c-8.448 16.64-14.848 34.304-19.2 52.48-4.352 18.176-6.528 36.864-6.528 56.064 0 52.992 38.4 99.84 92.16 124.928 4.224 1.984 8.512 3.52 12.8 4.608 14.592 4.352 30.208 6.528 46.08 6.528 56.32 0 105.472-24.064 139.904-66.56a321.792 321.792 0 0 0 23.552-29.696c3.52-4.608 6.528-9.728 9.216-15.36 2.688-5.632 4.608-11.712 5.888-18.176 1.408-6.656 1.92-13.568 0.512-20.48-0.384-1.792-0.896-3.456-1.536-5.12a254.336 254.336 0 0 1-21.248-55.296c-5.12-17.152-15.36-33.792-29.44-48.64a160.704 160.704 0 0 1-48.64-62.08c-15.616-25.6-38.144-47.488-64.0-64.512h378.88c8.96 0 16-7.04 16-16s-7.04-16-16-16H675.2c-1.792-5.632-4.096-10.752-6.528-15.36a48.128 48.128 0 0 0-4.096-5.632zM768 384c0 21.248-17.024 38.4-38.4 38.4H512c-21.248 0-38.4-17.024-38.4-38.4s17.024-38.4 38.4-38.4h217.6c21.248 0 38.4 17.024 38.4 38.4z" fill="#07C160"/></svg></el-icon>
              </div>
              <div class="payment-text">
                <div class="payment-name">微信支付</div>
                <div class="payment-desc">使用微信扫码支付</div>
              </div>
            </div>
          </el-radio>
          <el-radio :label="'alipay'" class="payment-option">
            <div class="payment-option-content">
              <div class="payment-icon alipay-icon">
                <el-icon><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="48" height="48"><path d="M760.192 180.224c-13.312-13.312-29.696-19.968-48.128-19.968H256c-18.432 0-34.816 6.656-48.128 19.968S176 210.24 176 232.576v591.232c0 22.336 6.656 38.72 19.968 48.128s29.696 19.968 48.128 19.968h477.312c18.432 0 34.816-6.656 48.128-19.968s19.968-25.792 19.968-48.128V232.576c0-22.336-6.656-38.72-19.968-48.128l-12.8-12.288zm-7.296 585.472c1.536 1.536 2.56 3.456 3.072 5.632-1.536 1.536-3.072 2.56-4.8 3.072-2.176 0.512-4.608 0.512-7.424 0l-419.328-26.048c-2.816 0-5.248 0-7.424-0.512-1.728-0.512-3.264-1.536-4.8-3.072 0.512-2.176 1.536-4.096 3.072-5.632L256 739.584v-486.912l277.056 17.408c2.816 0 5.248 0 7.424 0.512 1.728 0.512 3.264 1.536 4.8 3.072-0.512 2.176-1.536 4.096-3.072 5.632L256 267.456v472.192l496.896 31.488z" fill="#1677FF"/></svg></el-icon>
              </div>
              <div class="payment-text">
                <div class="payment-name">支付宝</div>
                <div class="payment-desc">使用支付宝扫码支付</div>
              </div>
            </div>
          </el-radio>
        </el-radio-group>
      </div>

      <!-- 支付按钮 -->
      <div class="submit-section">
        <el-button type="primary" size="large" @click="confirmPayment" :loading="paying" :disabled="!selectedPayment">
          确认支付
        </el-button>
      </div>
    </div>

    <!-- 无订单信息提示 -->
    <div v-else class="empty-tip">
      <el-empty description="未找到订单信息">
        <el-button type="primary" @click="goToMenu">返回菜单</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'

export default {
  name: 'Payment',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const orderId = ref('')
    const totalAmount = ref('0.00')
    const selectedPayment = ref('')
    const paying = ref(false)

    // 获取订单信息
    const fetchOrderInfo = async () => {
      // 从路由参数获取订单ID
      const id = route.query.order_id
      if (!id) {
        ElMessage.warning('订单ID无效')
        return
      }

      orderId.value = id
      
      // 尝试获取订单信息（可选）
      try {
        const response = await request.get(`/api/orders/${id}`)
        if (response.data) {
          totalAmount.value = response.data.total_amount || '0.00'
        }
      } catch (error) {
        console.log('获取订单信息失败，使用默认金额', error)
        // 如果获取失败，使用默认金额或从本地存储获取
        const amount = localStorage.getItem('payment_amount')
        if (amount) {
          totalAmount.value = amount
          localStorage.removeItem('payment_amount')
        }
      }
    }

    // 确认支付
    const confirmPayment = async () => {
      if (!selectedPayment.value) {
        ElMessage.warning('请选择支付方式')
        return
      }

      paying.value = true
      
      try {
        // 模拟支付过程
        await new Promise(resolve => setTimeout(resolve, 1500))

        // 更新订单状态为已支付
        await request.put(`/api/orders/${orderId.value}/status`, {
          status: 'PAID'
        })

        ElMessage.success('支付成功！')
        
        // 跳转到订单列表页
        router.push('/order-list')
      } catch (error) {
        console.error('支付失败:', error)
        ElMessage.error('支付失败，请稍后重试')
      } finally {
        paying.value = false
      }
    }

    // 返回菜单
    const goToMenu = () => {
      router.push('/menu')
    }

    onMounted(() => {
      fetchOrderInfo()
    })

    return {
      orderId,
      totalAmount,
      selectedPayment,
      paying,
      confirmPayment,
      goToMenu
    }
  }
}
</script>

<style scoped>
.payment-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.payment-header {
  margin-bottom: 20px;
}

.payment-header h2 {
  margin-bottom: 10px;
  color: #303133;
}

.payment-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-info-section,
.payment-method-section {
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

.order-info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 16px;
}

.order-info-item .amount {
  color: #D32F2F;
  font-size: 20px;
  font-weight: bold;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.payment-option {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  margin-right: 0;
  cursor: pointer;
  transition: all 0.3s;
}

.payment-option:hover {
  border-color: #c0c4cc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.payment-option.is-checked {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.payment-option-content {
  display: flex;
  align-items: center;
}

.payment-icon {
  margin-right: 15px;
}

.payment-icon .el-icon {
  font-size: 32px;
}

.payment-text {
  flex: 1;
}

.payment-name {
  font-size: 16px;
  color: #303133;
  margin-bottom: 5px;
}

.payment-desc {
  font-size: 14px;
  color: #909399;
}

.submit-section {
  text-align: right;
  padding-top: 20px;
}

.empty-tip {
  background-color: #fff;
  padding: 60px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 支付图标颜色 */
.steam-icon {
  color: #1b2838;
}

.wechat-icon {
  color: #07C160;
}

.alipay-icon {
  color: #1677FF;
}
</style>