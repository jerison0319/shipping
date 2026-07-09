<template>
  <div class="price-query-page">
    <el-row :gutter="24">
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header>
            <span><el-icon><Search /></el-icon> 配送价格查询</span>
          </template>

          <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
            <el-form-item label="国家" prop="country">
              <el-select v-model="form.country" placeholder="请选择国家" filterable style="width:100%">
                <el-option v-for="c in countries" :key="c.id" :label="c.name" :value="c.name" />
              </el-select>
            </el-form-item>

            <el-form-item label="商品价格" prop="productPrice">
              <el-input-number v-model="form.productPrice" :min="0" :precision="2" style="width:100%" />
            </el-form-item>

            <el-form-item label="商品类型" prop="productType">
              <el-select v-model="form.productType" placeholder="请选择商品类型" filterable style="width:100%">
                <el-option v-for="t in productTypes" :key="t.id" :label="t.name" :value="t.name" />
              </el-select>
            </el-form-item>

            <el-form-item label="长度单位" prop="lengthUnit">
              <el-select v-model="form.lengthUnit" style="width:100%">
                <el-option label="cm" value="cm" />
                <el-option label="inch" value="inch" />
              </el-select>
            </el-form-item>

            <el-form-item label="重量单位" prop="weightUnit">
              <el-select v-model="form.weightUnit" style="width:100%">
                <el-option label="g" value="g" />
                <el-option label="kg" value="kg" />
                <el-option label="lb" value="lb" />
                <el-option label="oz" value="oz" />
              </el-select>
            </el-form-item>

            <el-form-item label="长度" prop="length">
              <el-input-number v-model="form.length" :min="0" :precision="1" style="width:100%" />
            </el-form-item>

            <el-form-item label="宽度" prop="width">
              <el-input-number v-model="form.width" :min="0" :precision="1" style="width:100%" />
            </el-form-item>

            <el-form-item label="高度" prop="height">
              <el-input-number v-model="form.height" :min="0" :precision="1" style="width:100%" />
            </el-form-item>

            <el-form-item label="重量" prop="weight">
              <el-input-number v-model="form.weight" :min="0" :precision="2" style="width:100%" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" @click="handleQuery" :loading="querying" style="width:100%">
                <el-icon><Search /></el-icon> 查询价格
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="14">
        <el-card shadow="hover">
          <template #header>
            <span><el-icon><Document /></el-icon> 查询结果</span>
          </template>

          <div v-if="!result" class="no-result">
            <el-empty description="输入参数后点击查询" />
          </div>

          <div v-else class="result-content">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="国家" :span="1">
                <el-tag>{{ result.country }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="商品类型" :span="1">
                <el-tag type="success">{{ result.productType }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="产品等级">
                <el-tag type="warning">{{ result.productGrade }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="商品价格范围">
                {{ result.productPriceMin }} ~ {{ result.productPriceMax }}
              </el-descriptions-item>
              <el-descriptions-item label="单位">
                <el-tag size="small">{{ result.lengthUnit }}</el-tag> / <el-tag size="small">{{ result.weightUnit }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="配送价格" :span="2">
                <span class="price-value">{{ result.price }} {{ result.currency }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="备注" :span="2">
                {{ result.remark || '无' }}
              </el-descriptions-item>
              <el-descriptions-item label="输入参数" :span="2">
                <el-tag size="small">L:{{ form.length }}{{ form.lengthUnit }}</el-tag>
                <el-tag size="small" type="info">W:{{ form.width }}{{ form.lengthUnit }}</el-tag>
                <el-tag size="small" type="warning">H:{{ form.height }}{{ form.lengthUnit }}</el-tag>
                <el-tag size="small" type="danger">Wt:{{ form.weight }}{{ form.weightUnit }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>

            <div class="result-actions">
              <el-button type="primary" @click="copyResult">
                <el-icon><CopyDocument /></el-icon> 复制结果
              </el-button>
              <el-button @click="resetQuery">重新查询</el-button>
            </div>

            <el-divider />

            <div class="all-matches" v-if="result.all_matches && result.all_matches.length > 1">
              <h4>全部匹配规则 ({{ result.all_matches.length }} 条)</h4>
              <el-table :data="result.all_matches" stripe size="small" max-height="200">
                <el-table-column type="index" label="#" width="50" />
                <el-table-column prop="price" label="价格" width="100">
                  <template #default="{ row }">
                    {{ row.price }} {{ row.currency || result.currency }}
                  </template>
                </el-table-column>
                <el-table-column prop="remark" label="备注" />
              </el-table>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { queryPrice, getCountries, getProductTypes } from '../api/index.js'

const countries = ref([])
const productTypes = ref([])
const querying = ref(false)
const formRef = ref(null)
const result = ref(null)

const form = ref({
  country: '',
  productType: '',
  productPrice: 0,
  lengthUnit: 'cm',
  weightUnit: 'g',
  length: 0,
  width: 0,
  height: 0,
  weight: 0
})

const formRules = {
  country: [{ required: true, message: '请选择国家', trigger: 'change' }],
  productType: [{ required: true, message: '请选择商品类型', trigger: 'change' }],
  productPrice: [{ required: true, message: '请输入商品价格', trigger: 'blur' }, { type: 'number', message: '价格必须为数字', trigger: 'blur' }],
  length: [{ required: true, message: '请输入长度', trigger: 'blur' }],
  width: [{ required: true, message: '请输入宽度', trigger: 'blur' }],
  height: [{ required: true, message: '请输入高度', trigger: 'blur' }],
  weight: [{ required: true, message: '请输入重量', trigger: 'blur' }]
}

async function handleQuery() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  querying.value = true
  try {
    const res = await queryPrice(form.value)
    result.value = res.data
  } catch (e) {
    if (e.response?.status === 404) {
      result.value = null
      ElMessage.warning('未找到匹配的配送规则')
    }
  } finally {
    querying.value = false
  }
}

function resetQuery() {
  result.value = null
  form.value = { country: '', productType: '', productPrice: 0, lengthUnit: 'cm', weightUnit: 'g', length: 0, width: 0, height: 0, weight: 0 }
}

function copyResult() {
  if (!result.value) return
  const text = `国家: ${result.value.country}\n商品类型: ${result.value.productType}\n产品等级: ${result.value.productGrade}\n商品价格: ${result.value.productPriceMin} ~ ${result.value.productPriceMax}\n配送价格: ${result.value.price} ${result.value.currency}\n备注: ${result.value.remark || '无'}`
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('结果已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

onMounted(async () => {
  try {
    const [cRes, tRes] = await Promise.all([getCountries(), getProductTypes()])
    countries.value = cRes.data
    productTypes.value = tRes.data
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.price-query-page {
  max-width: 1200px;
  margin: 0 auto;
}

.no-result {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.result-content {
  min-height: 300px;
}

.price-value {
  font-size: 24px;
  font-weight: 700;
  color: #f56c6c;
}

.result-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.el-tag + .el-tag {
  margin-left: 4px;
}

.all-matches h4 {
  margin-bottom: 12px;
  color: #606266;
}

.dark .all-matches h4 {
  color: #c0c4cc;
}
</style>
