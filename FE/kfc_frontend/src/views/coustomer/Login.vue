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
        <!-- 用户名输入框,用prop向子组件传递信号，以下相同 -->
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="user"
            placeholder="请输入用户名" 
          />
        </el-form-item>
        <!-- 密码输入框,同时进行双向绑定,用缩写的v-on v-bind表示-->
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
// 6. 制作表单上的文字，检查是否填写，如果没有就输入文字，失去焦点时再次检查，整体用reactive包装让规则对象变成动态响应式
const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 1, message: '密码至少1位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
})

// 7. 登录按钮点击事件（直接注册逻辑）
const handleLogin = async () => {
  // 前端表单校验
  const valid = await loginFormRef.value.validate()
  if (!valid) return

  // 显示加载状态
  loginLoading.value = true

  try {
    // 调用后端登录接口（假设接口返回token字段）
    const res = await request.post('auth/user/users/login/', {
      username: loginForm.username,
      password: loginForm.password,
      role: loginForm.role
    })

    // 存储Token到本地（后端返回的token字段）
    localStorage.setItem('token', res.token) 
    localStorage.setItem('role', loginForm.role)

    if (loginForm.role === 'customer') {
      router.push('/menu')
    } else {
      router.push('/staff/order')
    }
    ElMessage.success('登录成功')
  } catch (error) {
    // 错误由request拦截器处理
  } finally {
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