<template>
  <div class="login-container">
    <!-- 登录卡片 -->
    <div class="login-card">
      <h2 class="login-title">KFC订单管理系统</h2>
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
            placeholder="请输入用户名" 
            prefix-icon="User"
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
  username: '', // 用户名（后端User表的username）
  password: '', // 密码（后端User表的password，加密存储）
  role: '' // 角色（customer/staff）
})
// 6. 表单验证规则（前端先校验，减少后端请求）
const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
})

// 7. 登录按钮点击事件
const handleLogin = async () => {
  // 第一步：前端校验表单（不通过则提示）
  const valid = await loginFormRef.value.validate()
  if (!valid) return

  // 第二步：显示加载状态
  loginLoading.value = true

  try {
    // 第三步：调用后端登录接口（接口地址按后端实际定义，这里假设是/login）
    const res = await request.post('/login', {
      username: loginForm.username,
      password: loginForm.password,
      role: loginForm.role
    })

    // 第四步：登录成功，存储Token和角色到本地
    localStorage.setItem('token', res.token) // 后端返回的Token
    localStorage.setItem('role', loginForm.role)

    // 第五步：根据角色跳对应页面
    if (loginForm.role === 'customer') {
      router.push('/menu') // 顾客跳菜单页
    } else {
      router.push('/staff/order') // 店员跳订单管理页
    }

    // 提示成功
    ElMessage.success('登录成功')
  } catch (error) {
    // 登录失败（如账号密码错），会被request的响应拦截器处理，这里不用额外写
  } finally {
    // 无论成功失败，关闭加载状态
    loginLoading.value = false
  }
}
</script>

<style scoped>
/* 登录页样式：居中显示 */
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
  color: #D32F2F; /* KFC红色 */
  margin-bottom: 20px;
}
.login-form {
  margin-top: 20px;
}
</style>