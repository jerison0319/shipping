<template>
  <el-container class="layout-container" :class="{ dark: isDark }">
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="sidebar-header">
        <div class="logo" v-if="!isCollapse">
          <el-icon :size="24"><Ship /></el-icon>
          <span class="logo-text">物流价格系统</span>
        </div>
        <el-icon v-else :size="24"><Ship /></el-icon>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        background-color="transparent"
        :router="true"
      >
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <div class="topbar-left">
          <el-icon
            class="collapse-btn"
            :size="20"
            @click="isCollapse = !isCollapse"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="topbar-right">
          <el-switch
            v-model="isDark"
            active-icon="MoonNight"
            inactive-icon="Sunny"
            @change="toggleDark"
            inline-prompt
          />
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Ship, Fold, Expand, MoonNight, Sunny } from '@element-plus/icons-vue'

const route = useRoute()
const isCollapse = ref(false)
const isDark = ref(localStorage.getItem('darkMode') === 'true')

const menuItems = [
  { path: '/dashboard', title: '首页', icon: 'HomeFilled' },
  { path: '/rules', title: '配送规则管理', icon: 'List' },
  { path: '/countries', title: '国家管理', icon: 'Flag' },
  { path: '/product-types', title: '商品类型管理', icon: 'Goods' },
  { path: '/price-query', title: '价格查询', icon: 'Search' }
]

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.title || ''
})

function toggleDark(val) {
  localStorage.setItem('darkMode', val)
  if (val) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

if (isDark.value) {
  document.documentElement.classList.add('dark')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  transition: background-color 0.3s;
}

.sidebar {
  background: #304156;
  transition: width 0.3s;
  overflow: hidden;
}

.dark .sidebar {
  background: #1d1e1f;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
}

.el-menu {
  border-right: none !important;
}

.el-menu-item {
  color: rgba(255,255,255,0.7) !important;
}
.el-menu-item.is-active {
  color: #409EFF !important;
  background: rgba(64,158,255,0.1) !important;
}
.el-menu-item:hover {
  background: rgba(255,255,255,0.05) !important;
}

.topbar {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
}

.dark .topbar {
  background: #1d1e1f;
  border-bottom-color: #333;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  cursor: pointer;
  color: #606266;
}
.dark .collapse-btn {
  color: #c0c4cc;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

.dark .main-content {
  background: #141414;
}
</style>
