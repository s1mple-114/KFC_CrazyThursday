<template>
  <div class="order-list-container">
    <div class="order-header">
      <h2>我的订单</h2>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><a href="/menu">菜单</a></el-breadcrumb-item>
        <el-breadcrumb-item>我的订单</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 筛选和操作 -->
    <div class="filter-section">
      <el-radio-group v-model="statusFilter" size="small" @change="fetchOrders">
        <el-radio-button :label="''">全部订单</el-radio-button>
        <el-radio-button :label="'PENDING'">待支付</el-radio-button>
        <el-radio-button :label="'PAID'">已支付</el-radio-button>
        <el-radio-button :label="'PREPARING'">制作中</el-radio-button>
        <el-radio-button :label="'READY'">待取餐</el-radio-button>
        <el-radio-button :label="'COMPLETED'">已完成</el-radio-button>
        <el-radio-button :label="'CANCELLED'">已取消</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 订单列表 -->
    <div class="order-list" v-if="orders.length > 0">
      <div v-for="order in orders" :key="order.id" class="order-item">
        <div class="order-header-info">
          <div class="order-id">订单号：{{ order.order_number || order.id }}</div>
          <div class="order-time">下单时间：{{ formatDateTime(order.created_time) }}</div>
          <div class="order-status">
            <span :class="`status-${getStatusClass(order.status)}`">{{ getStatusText(order.status) }}</span>
          </div>
        </div>
        
        <div class="order-items">
          <el-table :data="order.items" style="width: 100%" class="order-items-table">
            <el-table-column prop="product_name" label="商品名称" min-width="200"></el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
            <el-table-column prop="price" label="单价" width="120" align="center">
              <template #default="scope">
                ¥{{ scope.row.price.toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <div class="order-footer">
          <div class="order-remark" v-if="order.remark">
            <span class="remark-label">订单备注：</span>
            <span class="remark-content">{{ order.remark }}</span>
          </div>
          <div class="order-summary">
            <span class="total-quantity">共{{ getTotalQuantity(order) }}件商品</span>
            <span class="total-amount">合计：<span class="amount">¥{{ order.total_amount.toFixed(2) }}</span></span>
          </div>
          <div class="order-actions">
            <el-button type="primary" size="small" @click="viewOrderDetail(order.id)">查看详情</el-button>
            <el-button type="warning" size="small" v-if="order.status === 'PENDING'" @click="payOrder(order.id)">去支付</el-button>
            <el-button type="info" size="small" v-if="order.status === 'READY'" @click="confirmReceipt(order.id)">确认取餐</el-button>
            <el-button type="danger" size="small" v-if="order.status === 'PENDING'" @click="cancelOrder(order.id)">取消订单</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 无订单提示 -->
    <div class="empty-orders" v-else-if="!loading">
      <el-empty description="暂无订单">
        <el-button type="primary" @click="goToMenu">去逛逛</el-button>
      </el-empty>
    </div>

    <!-- 加载中 -->
    <div class="loading-container" v-else>
      <el-skeleton :rows="3" animated></el-skeleton>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="orders.length > 0">
      <el-pagination
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'OrderList',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const orders = ref([])
    const loading = ref(false)
    const statusFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const dialogVisible = ref(false)
    const currentOrder = ref(null)
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'PENDING': '待支付',
        'PAID': '已支付',
        'PREPARING': '制作中',
        'READY': '待取餐',
        'COMPLETED': '已完成',
        'CANCELLED': '已取消'
      }
      return statusMap[status] || status
    }
    
    // 获取状态样式类
    const getStatusClass = (status) => {
      const classMap = {
        'PENDING': 'warning',
        'PAID': 'info',
        'PREPARING': 'primary',
        'READY': 'success',
        'COMPLETED': 'success',
        'CANCELLED': 'danger'
      }
      return classMap[status] || 'default'
    }
    
    // 格式化日期时间
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // 计算订单总商品数量
    const getTotalQuantity = (order) => {
      return order.items.reduce((total, item) => total + item.quantity, 0)
    }
    
    // 获取订单列表
    const fetchOrders = async () => {
      loading.value = true
      try {
        const userId = localStorage.getItem('user_id')
        const response = await axios.get('/api/orders', {
          params: {
            user_id: userId,
            status: statusFilter.value || undefined,
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        orders.value = response.data.items || []
        total.value = response.data.total || 0
        
        // 如果有新订单ID参数，高亮显示新订单
        if (route.query.newOrderId && !loading.value) {
          ElMessage.success('订单创建成功！')
          // 清除URL参数，避免刷新页面再次显示提示
          router.replace({ query: {} })
        }
      } catch (error) {
        console.error('获取订单列表失败:', error)
        ElMessage.error('获取订单列表失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
    
    // 页面切换
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchOrders()
    }
    
    // 去菜单页面
    const goToMenu = () => {
      router.push('/menu')
    }
    
    // 查看订单详情
    const viewOrderDetail = async (orderId) => {
      try {
        const response = await axios.get(`/api/orders/${orderId}`)
        dialogVisible.value = true
        currentOrder.value = response.data
      } catch (error) {
        console.error('获取订单详情失败:', error)
        ElMessage.error('获取订单详情失败，请稍后重试')
      }
    }
    
    // 支付订单
    const payOrder = async (orderId) => {
      try {
        await axios.put(`/api/orders/${orderId}/status`, {
          status: 'PAID'
        })
        ElMessage.success('支付成功')
        fetchOrders()
      } catch (error) {
        console.error('支付失败:', error)
        ElMessage.error('支付失败，请稍后重试')
      }
    }
    
    // 确认取餐
    const confirmReceipt = async (orderId) => {
      try {
        await axios.put(`/api/orders/${orderId}/status`, {
          status: 'COMPLETED'
        })
        ElMessage.success('已确认取餐')
        fetchOrders()
      } catch (error) {
        console.error('确认取餐失败:', error)
        ElMessage.error('确认取餐失败，请稍后重试')
      }
    }
    
    // 取消订单
    const cancelOrder = async (orderId) => {
      try {
        await axios.put(`/api/orders/${orderId}/status`, {
          status: 'CANCELLED'
        })
        ElMessage.success('订单已取消')
        fetchOrders()
      } catch (error) {
        console.error('取消订单失败:', error)
        ElMessage.error('取消订单失败，请稍后重试')
      }
    }
    
    // 组件挂载时获取订单列表
    onMounted(() => {
      fetchOrders()
    })
    
    return {
      orders,
      loading,
      statusFilter,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      currentOrder,
      getStatusText,
      getStatusClass,
      getTotalQuantity,
      formatDateTime,
      handlePageChange,
      goToMenu,
      viewOrderDetail,
      payOrder,
      confirmReceipt,
      cancelOrder
    }
  }
}
</script>

<style scoped>
.order-list-container {
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

.filter-section {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-item {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.order-header-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #fafafa;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
  gap: 10px;
}

.order-time {
  color: #606266;
  font-size: 14px;
}

.order-id {
  font-weight: 500;
  color: #303133;
}

.order-status .status-warning {
  color: #e6a23c;
}

.order-status .status-info {
  color: #67c23a;
}

.order-status .status-primary {
  color: #409eff;
}

.order-status .status-success {
  color: #67c23a;
}

.order-status .status-danger {
  color: #f56c6c;
}

.order-address {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.address-label {
  color: #606266;
  margin-right: 5px;
}

.address-info {
  color: #303133;
}

.order-items {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.order-items-table {
  margin-bottom: 0;
}

.order-footer {
  padding: 15px 20px;
}

.order-remark {
  margin-bottom: 10px;
}

.remark-label {
  color: #606266;
  margin-right: 5px;
}

.remark-content {
  color: #303133;
}

.order-summary {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

.total-quantity {
  margin-right: 20px;
  color: #606266;
}

.total-amount {
  color: #606266;
}

.amount {
  color: #D32F2F;
  font-weight: bold;
  font-size: 18px;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.empty-orders {
  background-color: #fff;
  padding: 60px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>