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
app.mount('#app')
