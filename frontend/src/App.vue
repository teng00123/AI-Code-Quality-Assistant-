<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🤖 AI Code Quality Assistant</h1>
          <el-menu mode="horizontal" :default-active="activeMenu" @select="handleMenuSelect">
            <el-menu-item index="/dashboard">仪表板</el-menu-item>
            <el-menu-item index="/analysis">代码分析</el-menu-item>
            <el-menu-item index="/reports">分析报告</el-menu-item>
            <el-menu-item index="/settings">设置</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <div class="footer-content">
          <p>&copy; 2024 AI Code Quality Assistant. Made with ❤️ for better code.</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.path)

const handleMenuSelect = (key) => {
  router.push(key)
}
</script>

<style scoped>
#app {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.el-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px;
}
</style>