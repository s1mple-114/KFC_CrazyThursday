import { createApp } from 'vue'
import App from './App.vue'

// 1. 引入Pinia（关键：之前缺失的部分）
import { createPinia } from 'pinia'

// 引入Element Plus和样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 引入Element图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 2. 移除重复的token存储（同一key会覆盖，应在登录后动态存储）
// localStorage.setItem('token', '29c62eecd6525a5df397a102b03d54d0267066d4');
// localStorage.setItem('token', '433cbc683353096328dbff1b217b2a947016af24');

// 3. 创建Pinia实例
const pinia = createPinia()
const app = createApp(App)

// 全局注册Element图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 4. 注册依赖（顺序：Pinia → Element → 路由）
app.use(pinia) // 先注册Pinia
app.use(ElementPlus)
// 引入并使用路由
import router from './router'
app.use(router)

app.mount('#app')