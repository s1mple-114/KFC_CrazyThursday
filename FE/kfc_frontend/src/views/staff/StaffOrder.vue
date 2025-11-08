<template>
  <div class="staff-order-container">
    <h2>订单管理</h2>
    
    <!-- 搜索和筛选区域 -->
    <el-form :inline="true" class="search-form">
      <el-form-item label="订单状态">
        <el-select v-model="searchParams.status" placeholder="选择状态">
          <el-option label="全部" value=""></el-option>
          <el-option label="待支付" value="PENDING"></el-option>
          <el-option label="已支付" value="PAID"></el-option>
          <el-option label="制作中" value="PREPARING"></el-option>
          <el-option label="待取餐" value="READY"></el-option>
          <el-option label="已完成" value="COMPLETED"></el-option>
          <el-option label="已取消" value="CANCELLED"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchOrders">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 订单列表 -->
    <el-table :data="orderList" style="width: 100%">
      <el-table-column prop="order_number" label="订单号" width="180"></el-table-column>
      <el-table-column prop="user.username" label="顾客" width="120"></el-table-column>
      <el-table-column prop="total_amount" label="总金额" width="100">
        <template #default="scope">
          ¥{{ scope.row.total_amount }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="订单状态" width="120">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="payment_method" label="支付方式" width="120"></el-table-column>
      <el-table-column prop="created_time" label="下单时间" width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.created_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="completed_time" label="完成时间" width="180">
        <template #default="scope">
          {{ scope.row.completed_time ? formatDateTime(scope.row.completed_time) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button type="primary" size="small" @click="viewOrderDetail(scope.row.id)">查看详情</el-button>
          <el-button type="success" size="small" @click="updateOrderStatus(scope.row)" v-if="canUpdateStatus(scope.row.status)">更新状态</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    
    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="600px"
    >
      <div v-if="orderDetail">
        <h3>订单信息</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ orderDetail.order_number }}</el-descriptions-item>
          <el-descriptions-item label="顾客">{{ orderDetail.user?.username }}</el-descriptions-item>
          <el-descriptions-item label="总金额">¥{{ orderDetail.total_amount }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">{{ getStatusText(orderDetail.status) }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ orderDetail.payment_method }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatDateTime(orderDetail.created_time) }}</el-descriptions-item>
        </el-descriptions>
        
        <h3 style="margin-top: 20px">商品列表</h3>
        <el-table :data="orderDetail.order_items" style="width: 100%">
          <el-table-column prop="product.name" label="商品名称"></el-table-column>
          <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
          <el-table-column prop="price" label="单价" width="100">
            <template #default="scope">
              ¥{{ scope.row.price }}
            </template>
          </el-table-column>
          <el-table-column label="小计" width="100">
            <template #default="scope">
              ¥{{ (parseFloat(scope.row.price) * scope.row.quantity).toFixed(2) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
    
    <!-- 更新状态对话框 -->
    <el-dialog
      v-model="statusDialogVisible"
      title="更新订单状态"
      width="400px"
    >
      <el-form label-width="80px">
        <el-form-item label="当前状态">
          <el-tag :type="getStatusType(selectedOrder?.status)">{{ getStatusText(selectedOrder?.status) }}</el-tag>
        </el-form-item>
        <el-form-item label="新状态">
          <el-select v-model="newStatus" placeholder="选择新状态">
            <el-option
              v-for="option in getAvailableStatuses(selectedOrder?.status)"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="statusDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmStatusUpdate">确认更新</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import request from '../../utils/request'

export default {
  name: 'StaffOrder',
  data() {
    return {
      orderList: [],
      orderDetail: null,
      selectedOrder: null,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchParams: {
        status: ''
      },
      detailDialogVisible: false,
      statusDialogVisible: false,
      newStatus: ''
    }
  },
  mounted() {
    this.fetchOrders()
  },
  methods: {
    // 获取订单列表
    async fetchOrders() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          ...this.searchParams
        }
        
        const response = await request.get('/orders/orders/', { params })
        
        this.orderList = response.results || []
        this.total = response.count || 0
      } catch (error) {
        this.$message.error('获取订单列表失败：' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 搜索订单
    searchOrders() {
      this.currentPage = 1
      this.fetchOrders()
    },
    
    // 重置搜索
    resetSearch() {
      this.searchParams = {
        status: ''
      }
      this.fetchOrders()
    },
    
    // 分页处理
    handleSizeChange(size) {
      this.pageSize = size
      this.fetchOrders()
    },
    
    handleCurrentChange(current) {
      this.currentPage = current
      this.fetchOrders()
    },
    
    // 查看订单详情
    async viewOrderDetail(orderId) {
      try {
        const response = await request.get(`/orders/orders/${orderId}/`)
        
        this.orderDetail = response.data
        this.detailDialogVisible = true
      } catch (error) {
        this.$message.error('获取订单详情失败：' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 更新订单状态
    updateOrderStatus(order) {
      this.selectedOrder = order
      this.newStatus = ''
      this.statusDialogVisible = true
    },
    
    // 确认更新状态
    async confirmStatusUpdate() {
      if (!this.newStatus) {
        this.$message.warning('请选择新状态')
        return
      }
      
      try {
        await request.post(
          `/orders/orders/${this.selectedOrder.id}/update_status/`,
          { status: this.newStatus }
        )
        
        this.$message.success('订单状态更新成功')
        this.statusDialogVisible = false
        this.fetchOrders() // 重新获取订单列表
      } catch (error) {
        this.$message.error('更新状态失败：' + (error.response?.data?.detail || error.response?.data?.status?.[0] || error.message))
      }
    },
    
    // 获取状态类型（用于标签颜色）
    getStatusType(status) {
      const typeMap = {
        'PENDING': 'warning',
        'PAID': 'info',
        'PREPARING': 'primary',
        'READY': 'success',
        'COMPLETED': 'success',
        'CANCELLED': 'danger'
      }
      return typeMap[status] || 'default'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const textMap = {
        'PENDING': '待支付',
        'PAID': '已支付',
        'PREPARING': '制作中',
        'READY': '待取餐',
        'COMPLETED': '已完成',
        'CANCELLED': '已取消'
      }
      return textMap[status] || status
    },
    
    // 检查是否可以更新状态
    canUpdateStatus(status) {
      // 已完成和已取消的订单不能再更新状态
      return status !== 'COMPLETED' && status !== 'CANCELLED'
    },
    
    // 获取可用的状态选项
    getAvailableStatuses(currentStatus) {
      const statusOptions = [
        { label: '已支付', value: 'PAID' },
        { label: '制作中', value: 'PREPARING' },
        { label: '待取餐', value: 'READY' },
        { label: '已完成', value: 'COMPLETED' }
      ]
      
      // 根据当前状态过滤可用选项
      if (currentStatus === 'PENDING') {
        return statusOptions.filter(opt => opt.value === 'PAID')
      } else if (currentStatus === 'PAID') {
        return statusOptions.filter(opt => opt.value === 'PREPARING' || opt.value === 'COMPLETED')
      } else if (currentStatus === 'PREPARING') {
        return statusOptions.filter(opt => opt.value === 'READY' || opt.value === 'COMPLETED')
      } else if (currentStatus === 'READY') {
        return statusOptions.filter(opt => opt.value === 'COMPLETED')
      }
      
      return []
    },
    
    // 格式化日期时间
    formatDateTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.staff-order-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.staff-order-container h2 {
  margin-bottom: 20px;
  color: #303133;
}

.search-form {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.el-table {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>