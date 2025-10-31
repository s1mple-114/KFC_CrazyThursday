vue
  
<template>
  <el-container>
    <!-- 导航栏 -->
    <el-header style="background-color: #ffc72c; display: flex; justify-content: space-between; align-items: center;">
      <div style="font-size: 20px; font-weight: bold; color: #000;">KFC订单管理系统</div>
      <el-menu :default-active="activeIndex" mode="horizontal" background-color="#ffc72c" text-color="#000" active-text-color="#fff">
        <!-- 未登录时显示登录/注册 -->
        <el-menu-item index="1" v-if="!isLogin">登录</el-menu-item>
        <el-menu-item index="2" v-if="!isLogin">注册</el-menu-item>
        <!-- 登录后显示用户角色和退出 -->
        <el-menu-item index="3" v-if="isLogin">当前角色：{{ userRole }}</el-menu-item>
        <el-menu-item index="4" v-if="isLogin">退出登录</el-menu-item>
      </el-menu>
    </el-header>
  </el-container>
</template>

<script setup>
// 初始化数据：是否登录、用户角色
import { ref } from 'vue'
const isLogin = ref(false)  // false=未登录，true=已登录
const userRole = ref('')    // 存储角色：customer（顾客）/staff（店员）
const activeIndex = ref('1')
</script>

<style scoped>
.el-header {
  height: 60px !important;  /* 固定导航栏高度 */
}
</style>