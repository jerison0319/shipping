<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="card in statsCards" :key="card.title">
        <el-card shadow="hover" class="stats-card">
          <div class="stats-inner">
            <el-icon :size="32" :color="card.color">
              <component :is="card.icon" />
            </el-icon>
            <div class="stats-info">
              <span class="stats-value">{{ card.value }}</span>
              <span class="stats-label">{{ card.title }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="quick-actions" shadow="hover">
      <template #header>
        <span>快捷操作</span>
      </template>
      <div class="action-buttons">
        <el-button type="primary" @click="$router.push('/rules')">
          <el-icon><Plus /></el-icon>管理配送规则
        </el-button>
        <el-button type="success" @click="$router.push('/price-query')">
          <el-icon><Search /></el-icon>查询价格
        </el-button>
        <el-button type="warning" @click="$router.push('/countries')">
          <el-icon><Flag /></el-icon>管理国家
        </el-button>
        <el-button type="info" @click="$router.push('/product-types')">
          <el-icon><Goods /></el-icon>管理商品类型
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRules, getCountries, getProductTypes } from '../api/index.js'
import { Plus, Search, Flag, Goods } from '@element-plus/icons-vue'

const statsCards = ref([
  { title: '配送规则', value: 0, icon: 'List', color: '#409EFF' },
  { title: '国家/地区', value: 0, icon: 'Flag', color: '#67C23A' },
  { title: '商品类型', value: 0, icon: 'Goods', color: '#E6A23C' },
  { title: '系统状态', value: '运行中', icon: 'Monitor', color: '#909399' }
])

onMounted(async () => {
  try {
    const [rulesRes, countriesRes, typesRes] = await Promise.all([
      getRules({ page: 1, page_size: 1 }),
      getCountries(),
      getProductTypes()
    ])
    statsCards.value[0].value = rulesRes.data.total
    statsCards.value[1].value = countriesRes.data.length
    statsCards.value[2].value = typesRes.data.length
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
.stats-card {
  margin-bottom: 20px;
}
.stats-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stats-info {
  display: flex;
  flex-direction: column;
}
.stats-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}
.dark .stats-value {
  color: #e5eaf3;
}
.stats-label {
  font-size: 14px;
  color: #909399;
}
.quick-actions {
  margin-top: 20px;
}
.action-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
</style>


