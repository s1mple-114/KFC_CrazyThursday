<template>
  <div class="staff-product-container">
    <h2>商品管理</h2>
    
    <!-- 搜索和筛选区域 -->
    <el-form :inline="true" class="search-form">
      <el-form-item label="商品名称">
        <el-input v-model="searchParams.name" placeholder="输入商品名称"></el-input>
      </el-form-item>
      <el-form-item label="分类">
        <el-select v-model="searchParams.category" placeholder="选择分类">
          <el-option label="全部" value=""></el-option>
          <el-option label="汉堡" value="burger"></el-option>
          <el-option label="小吃" value="snack"></el-option>
          <el-option label="饮料" value="drink"></el-option>
          <el-option label="套餐" value="combo"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="searchParams.is_available" placeholder="选择状态">
          <el-option label="全部" value=""></el-option>
          <el-option label="上架" :value="true"></el-option>
          <el-option label="下架" :value="false"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchProducts">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
        <el-button type="success" @click="showAddDialog">添加商品</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 商品列表 -->
    <el-table :data="productList" style="width: 100%">
      <el-table-column type="index" label="序号" width="80"></el-table-column>
      <el-table-column prop="name" label="商品名称"></el-table-column>
      <el-table-column prop="category" label="分类" width="100">
        <template #default="scope">
          <el-tag>{{ getCategoryText(scope.row.category) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="价格" width="100">
        <template #default="scope">
          ¥{{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="is_available" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_available ? 'success' : 'danger'">
            {{ scope.row.is_available ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button type="primary" size="small" @click="showEditDialog(scope.row)">编辑</el-button>
          <el-button 
            :type="scope.row.is_available ? 'danger' : 'success'" 
            size="small" 
            @click="toggleProductStatus(scope.row)"
          >
            {{ scope.row.is_available ? '下架' : '上架' }}
          </el-button>
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
    
    <!-- 添加/编辑商品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '添加商品'"
      width="600px"
    >
      <el-form :model="productForm" :rules="rules" ref="productFormRef" label-width="100px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="productForm.category" placeholder="请选择分类">
            <el-option label="汉堡" value="burger"></el-option>
            <el-option label="小吃" value="snack"></el-option>
            <el-option label="饮料" value="drink"></el-option>
            <el-option label="套餐" value="combo"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input 
            v-model="productForm.price" 
            placeholder="请输入价格"
            type="number"
            :min="0"
            :step="0.01"
          ></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="productForm.description" 
            placeholder="请输入商品描述"
            type="textarea"
            :rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="是否上架" prop="is_available">
          <el-switch v-model="productForm.is_available"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确认</el-button>
      </template>
    </el-dialog>
    
    <!-- 确认对话框 -->
    <el-dialog
      v-model="confirmDialogVisible"
      title="确认操作"
      width="300px"
    >
      <p>{{ confirmMessage }}</p>
      <template #footer>
        <el-button @click="confirmDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAction">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import request from '../../utils/request'

export default {
  name: 'StaffProduct',
  data() {
    return {
      productList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchParams: {
        name: '',
        category: '',
        is_available: ''
      },
      dialogVisible: false,
      confirmDialogVisible: false,
      isEdit: false,
      selectedProduct: null,
      confirmMessage: '',
      confirmActionType: '',
      productForm: {
        id: null,
        name: '',
        category: '',
        price: '',
        description: '',
        is_available: true
      },
      rules: {
        name: [
          { required: true, message: '请输入商品名称', trigger: 'blur' },
          { min: 1, max: 100, message: '商品名称长度在1到100个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择商品分类', trigger: 'change' }
        ],
        price: [
          { required: true, message: '请输入商品价格', trigger: 'blur' },
          { type: 'number', min: 0, message: '价格必须大于等于0', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    // 获取商品列表
    async fetchProducts() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          ...this.searchParams
        }
        
        // 过滤空值参数
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await request.get('/products/products/', { params })
        
        this.productList = response.data.results || []
        this.total = response.data.count || 0
      } catch (error) {
        this.$message.error('获取商品列表失败：' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 搜索商品
    searchProducts() {
      this.currentPage = 1
      this.fetchProducts()
    },
    
    // 重置搜索
    resetSearch() {
      this.searchParams = {
        name: '',
        category: '',
        is_available: ''
      }
      this.fetchProducts()
    },
    
    // 分页处理
    handleSizeChange(size) {
      this.pageSize = size
      this.fetchProducts()
    },
    
    handleCurrentChange(current) {
      this.currentPage = current
      this.fetchProducts()
    },
    
    // 显示添加对话框
    showAddDialog() {
      this.isEdit = false
      this.productForm = {
        id: null,
        name: '',
        category: '',
        price: '',
        description: '',
        is_available: true
      }
      this.dialogVisible = true
    },
    
    // 显示编辑对话框
    showEditDialog(product) {
      this.isEdit = true
      this.productForm = {
        id: product.id,
        name: product.name,
        category: product.category,
        price: product.price,
        description: product.description || '',
        is_available: product.is_available
      }
      this.dialogVisible = true
    },
    
    // 提交表单
    async submitForm() {
      try {
        await this.$refs.productFormRef.validate()
        
        // 格式化价格，保留两位小数
        const formData = {
          ...this.productForm,
          price: parseFloat(this.productForm.price).toFixed(2)
        }
        
        let response
        if (this.isEdit) {
          // 更新商品
          response = await request.put(`/products/products/${formData.id}/`, formData)
          this.$message.success('商品更新成功')
        } else {
          // 创建商品
          delete formData.id
          response = await request.post('/products/products/', formData)
          this.$message.success('商品添加成功')
        }
        
        this.dialogVisible = false
        this.fetchProducts() // 重新获取商品列表
      } catch (error) {
        if (error.name === 'Error') {
          // 表单验证失败，不处理
          return
        }
        this.$message.error('操作失败：' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 切换商品状态
    toggleProductStatus(product) {
      this.selectedProduct = product
      this.confirmMessage = `确定要${product.is_available ? '下架' : '上架'}商品「${product.name}」吗？`
      this.confirmActionType = product.is_available ? '下架' : '上架'
      this.confirmDialogVisible = true
    },
    
    // 确认操作
    async confirmAction() {
      try {
        const formData = {
          ...this.selectedProduct,
          is_available: !this.selectedProduct.is_available
        }
        
        await request.put(`/products/products/${formData.id}/`, formData)
        
        this.$message.success(`商品${this.confirmActionType}成功`)
        this.confirmDialogVisible = false
        this.fetchProducts() // 重新获取商品列表
      } catch (error) {
        this.$message.error('操作失败：' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 获取分类文本
    getCategoryText(category) {
      const categoryMap = {
        'burger': '汉堡',
        'snack': '小吃',
        'drink': '饮料',
        'combo': '套餐'
      }
      return categoryMap[category] || category
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
.staff-product-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.staff-product-container h2 {
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