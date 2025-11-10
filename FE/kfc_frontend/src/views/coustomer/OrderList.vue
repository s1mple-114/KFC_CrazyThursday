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
      <el-radio-group v-model="statusFilter" size="small" @change="handleFilterChange" style="margin-bottom: 15px;">
        <el-radio-button :label="''">全部订单</el-radio-button>
        <el-radio-button :label="'PENDING'">待支付</el-radio-button>
        <el-radio-button :label="'PAID'">已支付</el-radio-button>
        <el-radio-button :label="'PREPARING'">制作中</el-radio-button>
        <el-radio-button :label="'READY'">待取餐</el-radio-button>
        <el-radio-button :label="'COMPLETED'">已完成</el-radio-button>
        <el-radio-button :label="'CANCELLED'">已取消</el-radio-button>
      </el-radio-group>
      <div style="display: flex; gap: 10px; margin-bottom: 10px;">
        <el-button type="primary" size="small" @click="forceRefreshFilter">强制刷新</el-button>
        <el-button type="info" size="small" @click="resetFilter">重置筛选</el-button>
        <el-tag type="success" size="small" v-if="statusFilter">
          当前筛选: {{ getStatusText(statusFilter) }}
        </el-tag>
        <el-tag type="info" size="small">
          订单数量: {{ orders.length }}
        </el-tag>
      </div>
      <div style="font-size: 12px; color: #606266; margin-bottom: 10px;">
        点击筛选按钮直接查看对应状态的订单，或点击强制刷新重新加载并应用筛选
      </div>
    </div>

    <!-- 订单列表 -->
    <div class="order-list" v-if="orders.length > 0">
      <div v-for="order in orders" :key="order.id" :class="['order-item', { 'highlight': highlightedOrderId && (String(order.id) === String(highlightedOrderId) || String(order.order_number) === String(highlightedOrderId)) }]">
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
import request from '../../utils/request'
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
    const highlightedOrderId = ref(null)
    
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
    
    // 处理筛选条件变化
    const resetFilter = () => {
      console.log('重置筛选条件')
      statusFilter.value = ''
      // 直接应用空筛选条件
      const allOrders = createMockOrders()
      orders.value = [...allOrders]
      total.value = allOrders.length
      ElMessage.success('已重置筛选条件，显示全部订单')
    }
    
    // 处理筛选条件变化 - 直接实现，不依赖其他方法
    const handleFilterChange = () => {
      console.log('筛选条件已变更为:', statusFilter.value)
      
      // 获取完整订单数据
      const allOrders = createMockOrders()
      
      // 执行筛选
      if (statusFilter.value && statusFilter.value.trim() !== '') {
        console.log(`执行筛选，状态: ${statusFilter.value}`)
        const filtered = allOrders.filter(order => {
          console.log(`检查订单ID: ${order.id}, 状态: ${order.status}`)
          return order.status === statusFilter.value
        })
        orders.value = filtered
        total.value = filtered.length
        console.log(`筛选完成，找到 ${filtered.length} 个订单`)
        ElMessage.success(`已筛选为${getStatusText(statusFilter.value)}，共${filtered.length}个订单`)
      } else {
        // 显示全部
        orders.value = [...allOrders]
        total.value = allOrders.length
        console.log('显示全部订单，数量:', allOrders.length)
        ElMessage.info('已显示全部订单')
      }
    }
    
    // 强制刷新筛选结果 - 直接实现
    const forceRefreshFilter = () => {
      console.log('执行强制刷新筛选')
      
      // 重新获取所有订单数据
      const allOrders = createMockOrders()
      
      // 直接应用当前筛选条件
      if (statusFilter.value && statusFilter.value.trim() !== '') {
        const filtered = allOrders.filter(order => order.status === statusFilter.value)
        orders.value = filtered
        total.value = filtered.length
        ElMessage.success(`已强制刷新筛选，当前显示${getStatusText(statusFilter.value)}，共${filtered.length}个订单`)
      } else {
        orders.value = [...allOrders]
        total.value = allOrders.length
        ElMessage.success('已强制刷新，显示全部订单')
      }
    }
    
    // 直接应用筛选的核心方法 - 简化版本
    const applyFilter = (orderData) => {
      const allOrders = orderData || createMockOrders()
      
      if (statusFilter.value && statusFilter.value.trim() !== '') {
        const filtered = allOrders.filter(order => order.status === statusFilter.value)
        orders.value = filtered
        total.value = filtered.length
      } else {
        orders.value = [...allOrders]
        total.value = allOrders.length
      }
    }
    
    // 获取订单列表
    const fetchOrders = async () => {
      loading.value = true
      try {
        // 检查URL参数，设置高亮订单ID
        if (route.query.newOrderId) {
          highlightedOrderId.value = route.query.newOrderId
          ElMessage.success('订单创建成功！')
          // 清除URL参数，避免刷新页面再次显示提示
          setTimeout(() => {
            router.replace({ query: {} })
            highlightedOrderId.value = null
          }, 3000)
        }
        
        console.log('加载订单数据并应用当前筛选条件')
        
        // 直接使用模拟数据并应用当前筛选条件
        const mockOrders = createMockOrders()
        
        // 处理可能的新订单和localStorage订单
        let finalOrders = [...mockOrders]
        
        // 如果有新订单参数
        if (route.query.newOrderId) {
          const newOrderId = route.query.newOrderId
          finalOrders.unshift({
            id: newOrderId,
            order_number: `ORD${new Date().toISOString().slice(0, 10).replace(/-/g, '')}${Date.now().toString().slice(-6)}`,
            user: { id: 1, username: 'frontend' },
            status: 'PENDING',
            payment_method: 'ALIPAY',
            total_amount: 68.50,
            shipping_address: '广东海洋大学牢大区',
            created_time: new Date().toISOString(),
            updated_time: new Date().toISOString(),
            remark: '',
            items: [
              { product_name: '新奥尔良烤翅', quantity: 2, price: 14.50 },
              { product_name: '香辣鸡腿堡', quantity: 1, price: 25.00 },
              { product_name: '薯条(大)', quantity: 1, price: 16.00 },
              { product_name: '可乐(大)', quantity: 1, price: 13.00 }
            ]
          })
        }
        
        // 从localStorage获取已更新状态的订单信息
        try {
          const currentOrderStr = localStorage.getItem('currentOrder')
          if (currentOrderStr) {
            const currentOrder = JSON.parse(currentOrderStr)
            if (currentOrder.id) {
              const orderIndex = finalOrders.findIndex(order => String(order.id) === String(currentOrder.id))
              if (orderIndex !== -1) {
                finalOrders[orderIndex] = currentOrder
              } else {
                finalOrders.unshift(currentOrder)
              }
            }
          }
        } catch (e) {
          console.error('localStorage读取失败:', e)
        }
        
        // 直接应用当前筛选条件
        if (statusFilter.value && statusFilter.value.trim() !== '') {
          console.log(`应用筛选条件: ${statusFilter.value}`)
          orders.value = finalOrders.filter(order => order.status === statusFilter.value)
          total.value = orders.value.length
        } else {
          orders.value = finalOrders
          total.value = finalOrders.length
        }
        
      } catch (error) {
        console.error('获取订单列表失败:', error)
        ElMessage.error('获取订单列表失败，请刷新页面重试')
      } finally {
        loading.value = false
      }
    }
    
    // 创建完整的模拟订单数据，包含各种状态的订单
    const createMockOrders = () => {
      console.log('创建模拟订单数据')
      const orders = [
        {
          id: 1,
          order_number: 'ORD202411090001',
          user: { id: 1, username: 'frontend' },
          status: 'COMPLETED',
          payment_method: 'ALIPAY',
          total_amount: 89.50,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-09T10:30:00Z',
          updated_time: '2024-11-09T11:00:00Z',
          remark: '不要辣',
          items: [
            { product_name: '香辣鸡腿堡', quantity: 2, price: 25.00 },
            { product_name: '薯条(中)', quantity: 1, price: 13.50 },
            { product_name: '可乐(中)', quantity: 2, price: 9.00 }
          ]
        },
        {
          id: 2,
          order_number: 'ORD202411080002',
          user: { id: 1, username: 'frontend' },
          status: 'PENDING',
          payment_method: 'WECHAT',
          total_amount: 56.00,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-08T18:20:00Z',
          updated_time: '2024-11-08T18:20:00Z',
          remark: '',
          items: [
            { product_name: '奥尔良烤鸡腿堡', quantity: 1, price: 28.00 },
            { product_name: '原味鸡', quantity: 2, price: 14.00 }
          ]
        },
        {
          id: 3,
          order_number: 'ORD202411070003',
          user: { id: 1, username: 'frontend' },
          status: 'READY',
          payment_method: 'ALIPAY',
          total_amount: 42.00,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-07T12:15:00Z',
          updated_time: '2024-11-07T12:25:00Z',
          remark: '多加番茄酱',
          items: [
            { product_name: '嫩牛五方', quantity: 1, price: 23.00 },
            { product_name: '鸡米花(中)', quantity: 1, price: 11.00 },
            { product_name: '雪碧(中)', quantity: 1, price: 8.00 }
          ]
        },
        {
          id: 4,
          order_number: 'ORD202411060004',
          user: { id: 1, username: 'frontend' },
          status: 'PREPARING',
          payment_method: 'ALIPAY',
          total_amount: 35.50,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-06T19:30:00Z',
          updated_time: '2024-11-06T19:32:00Z',
          remark: '',
          items: [
            { product_name: '香辣鸡翅', quantity: 2, price: 12.50 },
            { product_name: '薯条(小)', quantity: 1, price: 10.50 }
          ]
        },
        {
          id: 5,
          order_number: 'ORD202411050005',
          user: { id: 1, username: 'frontend' },
          status: 'CANCELLED',
          payment_method: '',
          total_amount: 78.00,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-05T12:00:00Z',
          updated_time: '2024-11-05T12:05:00Z',
          remark: '临时有事',
          items: [
            { product_name: '家庭套餐', quantity: 1, price: 78.00 }
          ]
        },
        {
          id: 6,
          order_number: 'ORD202411040006',
          user: { id: 1, username: 'frontend' },
          status: 'PAID',
          payment_method: 'WECHAT',
          total_amount: 68.50,
          shipping_address: '广东海洋大学牢大区',
          created_time: '2024-11-04T18:45:00Z',
          updated_time: '2024-11-04T18:46:00Z',
          remark: '尽快送达',
          items: [
            { product_name: '新奥尔良烤翅', quantity: 2, price: 14.50 },
            { product_name: '香辣鸡腿堡', quantity: 1, price: 25.00 },
            { product_name: '可乐(大)', quantity: 1, price: 13.00 }
          ]
        }
      ]
      console.log('模拟订单数据创建完成，包含订单数量:', orders.length)
      console.log('各订单状态分布:', orders.map(o => o.status).join(', '))
      return orders
    }
    
    // 实现订单分类筛选逻辑
    const filterOrdersByStatus = (allOrders) => {
      console.log('执行订单筛选，状态筛选条件:', statusFilter.value)
      console.log('筛选前所有订单数量:', allOrders.length)
      console.log('订单状态分布:', JSON.stringify(allOrders.map(o => o.status)))
      
      // 确保orders是响应式的
      if (!Array.isArray(allOrders)) {
        console.error('筛选数据不是数组:', allOrders)
        orders.value = []
        total.value = 0
        return
      }
      
      // 根据状态筛选 - 使用新的变量存储筛选结果，然后赋值给orders.value
      let filteredOrders = []
      
      if (statusFilter.value && statusFilter.value.trim() !== '') {
        console.log(`筛选条件: ${statusFilter.value}`)
        filteredOrders = allOrders.filter(order => {
          const orderStatus = order.status || ''
          const matchResult = orderStatus === statusFilter.value
          console.log(`订单ID: ${order.id}, 状态: ${orderStatus}, 是否匹配: ${matchResult}`)
          return matchResult
        })
        console.log(`筛选后订单数量: ${filteredOrders.length}，状态: ${getStatusText(statusFilter.value)}`)
        console.log(`筛选状态: ${statusFilter.value}，匹配的订单ID:`, JSON.stringify(filteredOrders.map(o => o.id)))
      } else {
        filteredOrders = [...allOrders]
        console.log('显示全部订单，数量:', filteredOrders.length)
      }
      
      // 确保重新赋值给orders.value，触发响应式更新
      orders.value = filteredOrders
      total.value = filteredOrders.length
      console.log('筛选完成，最终订单数量:', orders.value.length)
    }
    
    // 设置模拟订单数据
    const setMockOrderData = () => {
      console.log('开始设置模拟订单数据')
      // 获取完整的模拟订单数据
      let mockOrders = createMockOrders()
      
      // 如果有新订单ID参数，将其添加为最新订单
      if (route.query.newOrderId) {
        const newOrderId = route.query.newOrderId
        mockOrders.unshift({
          id: newOrderId,
          order_number: `ORD${new Date().toISOString().slice(0, 10).replace(/-/g, '')}${Date.now().toString().slice(-6)}`,
          user: { id: 1, username: 'frontend' },
          status: 'PENDING',
          payment_method: 'ALIPAY',
          total_amount: 68.50,
          shipping_address: '广东海洋大学牢大区',
          created_time: new Date().toISOString(),
          updated_time: new Date().toISOString(),
          remark: '',
          items: [
            { product_name: '新奥尔良烤翅', quantity: 2, price: 14.50 },
            { product_name: '香辣鸡腿堡', quantity: 1, price: 25.00 },
            { product_name: '薯条(大)', quantity: 1, price: 16.00 },
            { product_name: '可乐(大)', quantity: 1, price: 13.00 }
          ]
        })
        console.log('添加了新订单，当前订单总数:', mockOrders.length)
      }
      
      // 从localStorage获取已更新状态的订单信息
      try {
        const currentOrderStr = localStorage.getItem('currentOrder')
        if (currentOrderStr) {
          const currentOrder = JSON.parse(currentOrderStr)
          // 查找订单列表中是否存在相同ID的订单
          const orderIndex = mockOrders.findIndex(order => String(order.id) === String(currentOrder.id))
          if (orderIndex !== -1) {
            // 更新订单状态
            mockOrders[orderIndex] = currentOrder
            console.log('已从localStorage更新订单状态:', currentOrder)
          } else if (currentOrder.id) {
            // 如果订单不存在，添加新订单
            mockOrders.unshift(currentOrder)
            console.log('已从localStorage添加新订单:', currentOrder)
          }
        }
      } catch (parseError) {
        console.error('解析localStorage订单信息失败:', parseError)
      }
      
      // 使用新的applyFilter方法
      applyFilter(mockOrders)
      
      console.log(`已加载模拟订单数据，筛选条件: ${statusFilter.value || '全部'}，订单数量: ${orders.value.length}`)
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
        const response = await request.get(`/orders/orders/${orderId}/`)
        dialogVisible.value = true
        currentOrder.value = response.data
      } catch (error) {
        console.error('获取订单详情失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        ElMessage.error('获取订单详情失败，请稍后重试')
      }
    }
    
    // 支付订单
    const payOrder = async (orderId) => {
      try {
        // 从订单列表中获取订单信息
        const order = orders.value.find(order => String(order.id) === String(orderId))
        if (order) {
          // 保存订单信息到localStorage，供支付页面使用
          localStorage.setItem('currentOrder', JSON.stringify(order))
          // 跳转到支付页面
          router.push({
            path: '/payment',
            query: { orderId: orderId, amount: order.total_amount }
          })
        } else {
          console.error('未找到订单信息:', orderId)
          ElMessage.error('找不到订单信息，请刷新页面重试')
        }
      } catch (error) {
        console.error('支付处理失败:', error)
        ElMessage.error('支付过程中出现问题，请稍后重试')
      }
    }
    
    // 确认取餐
    const confirmReceipt = async (orderId) => {
      try {
        // 尝试调用后端API确认取餐
        try {
          await request.post(`/orders/orders/${orderId}/update_status/`, {
            status: 'COMPLETED'
          })
          ElMessage.success('已确认取餐')
          // 后端API调用成功时刷新列表
          fetchOrders()
        } catch (apiError) {
          console.error('API调用失败，模拟确认取餐成功:', apiError)
          
          // 模拟确认取餐成功
          ElMessage({ message: '使用演示模式，模拟确认取餐成功', type: 'success' })
          
          // 直接在前端更新订单状态
          const orderIndex = orders.value.findIndex(order => String(order.id) === String(orderId))
          if (orderIndex !== -1) {
            orders.value[orderIndex].status = 'COMPLETED'
            // 更新订单时间
            const now = new Date().toISOString()
            orders.value[orderIndex].updated_time = now
            console.log('订单状态已更新:', orders.value[orderIndex])
          } else {
            console.error('未找到要更新的订单:', orderId)
          }
          // 模拟模式下不刷新列表，避免重置数据
        }
      } catch (error) {
        console.error('确认取餐处理失败:', error)
        ElMessage.error('确认取餐过程中出现问题，请稍后重试')
      }
    }
    
    // 取消订单
    const cancelOrder = async (orderId) => {
      try {
        // 尝试调用后端API取消订单
        try {
          await request.post(`/orders/orders/${orderId}/update_status/`, {
            status: 'CANCELLED'
          })
          ElMessage.success('订单已取消')
          // 后端API调用成功时刷新列表
          fetchOrders()
        } catch (apiError) {
          console.error('API调用失败，模拟取消订单成功:', apiError)
          
          // 模拟取消订单成功
          ElMessage({ message: '使用演示模式，模拟取消订单成功', type: 'success' })
          
          // 直接在前端更新订单状态
          const orderIndex = orders.value.findIndex(order => String(order.id) === String(orderId))
          if (orderIndex !== -1) {
            orders.value[orderIndex].status = 'CANCELLED'
            // 更新订单时间
            const now = new Date().toISOString()
            orders.value[orderIndex].updated_time = now
            console.log('订单状态已更新:', orders.value[orderIndex])
          } else {
            console.error('未找到要更新的订单:', orderId)
          }
          // 模拟模式下不刷新列表，避免重置数据
        }
      } catch (error) {
        console.error('取消订单处理失败:', error)
        ElMessage.error('取消订单过程中出现问题，请稍后重试')
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
      highlightedOrderId,
      getStatusText,
      getStatusClass,
      getTotalQuantity,
      formatDateTime,
      handlePageChange,
      goToMenu,
      viewOrderDetail,
      payOrder,
      confirmReceipt,
      cancelOrder,
      handleFilterChange,
      forceRefreshFilter,
      applyFilter,
      resetFilter // 导出重置筛选方法
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
    transition: all 0.3s ease;
  }
  
  .order-item.highlight {
    background-color: #f0f9ff;
    border: 2px solid #409eff;
    box-shadow: 0 4px 8px rgba(64, 158, 255, 0.2);
    animation: pulse 2s ease-in-out;
  }
  
  @keyframes pulse {
    0% {
      box-shadow: 0 4px 8px rgba(64, 158, 255, 0.2);
    }
    50% {
      box-shadow: 0 4px 20px rgba(64, 158, 255, 0.4);
    }
    100% {
      box-shadow: 0 4px 8px rgba(64, 158, 255, 0.2);
    }
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