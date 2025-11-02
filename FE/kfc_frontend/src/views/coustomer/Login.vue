vue
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
            prefix-icon="User"
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
// 假设request已全局引入，若未引入需补充：import request from '@/utils/request'
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
// 6. 表单验证规则
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

// 7. 登录按钮点击事件（核心修改：登录即注册逻辑）
const handleLogin = async () => {
  // 第一步：前端表单校验
  const valid = await loginFormRef.value.validate()
  if (!valid) return

  // 第二步：显示加载状态
  loginLoading.value = true

  try {
    // 第三步：先查询用户是否已存在（需后端提供查询接口，假设为/user/exists）
    const existsRes = await request.get('/user/exists', {
      params: { username: loginForm.username, role: loginForm.role }
    })

    let res
    // 第四步：判断用户是否存在，不存在则注册，存在则登录
    if (!existsRes.data) {
      // 新用户：调用注册接口（需后端提供注册接口，假设为/register）
      await request.post('/register', {
        username: loginForm.username,
        password: loginForm.password,
        role: loginForm.role
      })
      ElMessage.info('账号已自动注册，正在登录...')
      
      // 注册后执行登录
      res = await request.post('/login', {
        username: loginForm.username,
        password: loginForm.password,
        role: loginForm.role
      })
    } else {
      // 老用户：直接执行登录
      res = await request.post('/login', {
        username: loginForm.username,
        password: loginForm.password,
        role: loginForm.role
      })
    }

    // 第五步：登录成功，存储Token和角色
    localStorage.setItem('token', res.data.token) // 注意：根据后端返回结构调整（可能是res.token）
    localStorage.setItem('role', loginForm.role)

    // 第六步：根据角色跳转页面
    if (loginForm.role === 'customer') {
      router.push('/menu')
    } else {
      router.push('/staff/order')
    }

    ElMessage.success('登录成功')
  } catch (error) {
    // 错误提示（覆盖后端未处理的异常）
    ElMessage.error(error.message || '登录失败，请重试')
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