<template>
  <div class="login-container">
    <!-- 登录卡片 -->
    <div class="login-card">
      <h2 class="login-title">欢迎光临KFC</h2>
      <h2 class="login-title">请登录你的账号，系统将自动注册</h2>
      <!-- 登录表单 -->
      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="loginRules" 
        label-width="80px"
        class="login-form"
      >
        <!-- 用户名输入框 -->
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="user"
            placeholder="请输入用户名" 
          />
        </el-form-item>
        <!-- 密码输入框 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            :show-password="showPwd"
            @click:icon="showPwd = !showPwd"
          />
        </el-form-item>
        <!-- 角色选择 -->
        <el-form-item label="角色" prop="role">
          <el-select 
            v-model="loginForm.role" 
            placeholder="请选择角色"
            style="width: 100%"
          >
            <el-option label="顾客" value="customer"></el-option>
            <el-option label="店员" value="staff"></el-option>
          </el-select>
        </el-form-item>
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleLogin" 
            style="width: 100%"
            :loading="loginLoading"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
// request引入
import request from '../../utils/request'
// 1. 路由实例
const router = useRouter()
// 2. 表单引用（用于表单验证）
const loginFormRef = ref(null)
// 3. 登录加载状态（按钮loading）
const loginLoading = ref(false)
// 4. 显示/隐藏密码
const showPwd = ref(false)
// 5. 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  role: ''
})
const handleLogin = async () => {
  // 前端表单校验
  try {
    await loginFormRef.value.validate()
  } catch (error) {
    return // 校验失败，终止执行
  }

  loginLoading.value = true

  try {
    // 1. 先尝试注册
    await request.post('/auth/users/register/', {
      username: loginForm.username,
      password: loginForm.password,
      role: loginForm.role
    })
    ElMessage.success('注册成功，正在登录...')
  } catch (error) {
    // 2. 注册失败：判断是否是“用户已存在”错误（根据后端实际返回调整）
    if (!(error.response?.data?.message?.includes('已存在'))) {
      // 非“已存在”错误（如注册参数错误），直接终止并显示错误（拦截器已处理提示）
      loginLoading.value = false
      return
    }
    // 若为“已存在”错误，继续执行登录流程
    ElMessage.info('用户已存在，直接登录...')
  }

  try {
    // 3. 执行登录（无论注册成功还是用户已存在，都走到登录步骤）
    const loginRes = await request.post('/auth/users/login/', {
      username: loginForm.username,
      password: loginForm.password,
      role: loginForm.role
    })

    // 登录成功处理
    localStorage.setItem('token', loginRes.token)
    localStorage.setItem('role', loginForm.role)
    ElMessage.success('登录成功')
    router.push(loginForm.role === 'customer' ? '/Menu' : '/staff/order')
  } catch (error) {
    // 登录失败（如密码错误等，拦截器已处理提示）
  } finally {
    // 关闭加载状态
    loginLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-card {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.login-title {
  text-align: center;
  color: #D32F2F;
  margin-bottom: 20px;
}
.login-form {
  margin-top: 20px;
}
</style>