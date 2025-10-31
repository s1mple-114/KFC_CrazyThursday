avascript
  
import { createApp } from 'vue'
import App from './App.vue'
// 引入Element Plus和样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 引入Element图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
// 全局注册Element图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
// 全局使用Element Plus
app.use(ElementPlus)
// 新增：引入路由
import router from './router'
// 新增：使用路由
app.use(router)
app.mount('#app')
