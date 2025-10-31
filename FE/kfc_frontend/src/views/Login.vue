vue
  
<template>
  <el-container style="height: 100vh; background-color: #f5f5f5;">
    <!-- 导航栏 -->
    <Navbar />
    <!-- 登录表单 -->
    <el-main style="display: flex; justify-content: center; align-items: center;">
      <el-card style="width: 400px; padding: 20px;">
        <div style="text-align: center; font-size: 24px; margin-bottom: 20px; font-weight: bold;">用户登录</div>
        <el-form :model="loginForm" label-width="80px">
          <!-- 用户名输入框 -->
          <el-form-item label="用户名">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <!-- 密码输入框 -->
          <el-form-item label="密码">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <!-- 角色选择 -->
          <el-form-item label="角色">
            <el-select v-model="loginForm.role" placeholder="选择角色">
              <el-option label="顾客" value="customer"></el-option>
              <el-option label="店员" value="staff"></el-option>
            </el-select>
          </el-form-item>
          <!-- 登录按钮 -->
          <el-form-item>
            <el-button type="primary" style="width: 100%;" @click="handleLogin">登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
// 引入导航栏组件
import Navbar from '../components/Navbar.vue'
// 引入Vue的响应式数据和路由（后面会配置路由）
import { ref } from 'vue'

// 登录表单数据
const loginForm = ref({
  username: '',    // 用户名
  password: '',    // 密码
  role: 'customer' // 默认角色：顾客
})

// 登录按钮点击事件（暂时只做弹窗提示，后面连后端再改）
const handleLogin = () => {
  if (loginForm.value.username === '' || loginForm.value.password === '') {
    // 弹窗提示“请填用户名密码”
    ElMessage.warning('请输入用户名和密码！')
  } else {
    // 弹窗提示“登录成功”
    ElMessage.success('登录成功！')
    // 这里后面会加“跳转到对应页面”的代码
  }
}
</script>