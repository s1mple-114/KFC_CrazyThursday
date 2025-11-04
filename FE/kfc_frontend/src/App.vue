<template>
  <!-- 所有页面通过 router-view 渲染 -->
  <router-view />
</template>

<script setup>

</script>
<style scoped>
/* 只保留全局基础样式，避免复杂样式冲突 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* 统一盒模型，避免布局错乱 */
}
body {
  font-family: 'Microsoft YaHei', sans-serif;
  background-color: #f5f5f5; /* 加个背景色，方便区分页面 */
}
</style>