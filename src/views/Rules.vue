<template>
  <div class="rules-page">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span>配送规则列表</span>
          <div class="header-actions">
            <el-upload
              :show-file-list="false"
              :before-upload="handleImport"
              accept=".xlsx,.xls"
            >
              <el-button size="small">
                <el-icon><Upload /></el-icon>导入Excel
              </el-button>
            </el-upload>
            <el-button size="small" type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" size="small" @click="openAddDialog">
              <el-icon><Plus /></el-icon>新增规则
            </el-button>
          </div>
        </div>
      </template>

      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索国家/商品类型/备注"
          clearable
          size="small"
          style="width: 240px"
          @clear="fetchRules"
          @keyup.enter="fetchRules"
        />
        <el-select
          v-model="filterCountry"
          placeholder="选择国家"
          clearable
          size="small"
          style="width: 160px"
          @change="fetchRules"
        >
          <el-option v-for="c in countries" :key="c.id" :label="c.name" :value="c.name" />
        </el-select>
        <el-select
          v-model="filterProductType"
          placeholder="选择商品类型"
          clearable
          size="small"
          style="width: 160px"
          @change="fetchRules"
        >
          <el-option v-for="t in productTypes" :key="t.id" :label="t.name" :value="t.name" />
        </el-select>
        <el-button size="small" @click="resetFilters">重置</el-button>
      </div>

      <el-table
        :data="rules"
        stripe
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
        v-loading="loading"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column prop="country" label="国家" width="100" sortable="custom" />
        <el-table-column prop="productType" label="商品类型" width="120" sortable="custom" />
        <el-table-column prop="productGrade" label="产品等级" width="100" />
        <el-table-column label="商品价格范围" width="140">
          <template #default="{ row }">
            {{ row.productPriceMin }} ~ {{ row.productPriceMax }}
          </template>
        </el-table-column>
        <el-table-column label="长宽高范围" min-width="200">
          <template #default="{ row }">
            L:{{ row.lengthMin }}~{{ row.lengthMax }}{{ row.lengthUnit }}
            W:{{ row.widthMin }}~{{ row.widthMax }}{{ row.widthUnit }}
            H:{{ row.heightMin }}~{{ row.heightMax }}{{ row.heightUnit }}
          </template>
        </el-table-column>
        <el-table-column label="重量范围" width="120">
          <template #default="{ row }">
            {{ row.weightMin }}~{{ row.weightMax }}{{ row.weightUnit }}
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="80" sortable="custom">
          <template #default="{ row }">
            {{ row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="currency" label="币种" width="80" />
        <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openEditDialog(row)">
              编辑
            </el-button>
            <el-popconfirm title="确认删除该规则？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <div class="batch-actions">
          <el-button
            size="small"
            type="danger"
            :disabled="selectedIds.length === 0"
            @click="handleBatchDelete"
          >
            批量删除 ({{ selectedIds.length }})
          </el-button>
        </div>
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="fetchRules"
          @current-change="fetchRules"
        />
      </div>
    </el-card>

    <!-- Add/Edit Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑规则' : '新增规则'"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="120px"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="国家" prop="country">
              <el-select v-model="form.country" @change="handleCountryChange" placeholder="请选择国家" filterable style="width:100%">
                <el-option v-for="c in countries" :key="c.id" :label="c.name" :value="c.name" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="商品类型" prop="productType">
              <el-select v-model="form.productType" placeholder="请选择商品类型" filterable style="width:100%">
                <el-option v-for="t in productTypes" :key="t.id" :label="t.name" :value="t.name" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="产品等级" prop="productGrade">
              <el-input v-model="form.productGrade" placeholder="请输入产品等级" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-col :span="12">
            <el-form-item label="商品价格 Min" prop="productPriceMin">
              <el-input-number v-model="form.productPriceMin" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="商品价格 Max" prop="productPriceMax">
              <el-input-number v-model="form.productPriceMax" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="长度单位" prop="lengthUnit">
              <el-select v-model="form.lengthUnit" style="width:100%">
                <el-option label="cm" value="cm" />
                <el-option label="inch" value="inch" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="重量单位" prop="weightUnit">
              <el-select v-model="form.weightUnit" style="width:100%">
                <el-option label="g" value="g" />
                <el-option label="kg" value="kg" />
                <el-option label="lb" value="lb" />
                <el-option label="oz" value="oz" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="长度 Min" prop="lengthMin">
              <el-input-number v-model="form.lengthMin" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="长度 Max" prop="lengthMax">
              <el-input-number v-model="form.lengthMax" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="宽度 Min" prop="widthMin">
              <el-input-number v-model="form.widthMin" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="宽度 Max" prop="widthMax">
              <el-input-number v-model="form.widthMax" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="高度 Min" prop="heightMin">
              <el-input-number v-model="form.heightMin" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="高度 Max" prop="heightMax">
              <el-input-number v-model="form.heightMax" :min="0" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="重量 Min" prop="weightMin">
              <el-input-number v-model="form.weightMin" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="重量 Max" prop="weightMax">
              <el-input-number v-model="form.weightMax" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="价格" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="币种" prop="currency">
              <el-input v-model="form.currency" placeholder="请输入币种，如 USD" />

            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="备注">
              <el-input v-model="form.remark" placeholder="可选" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getRules, createRule, updateRule, deleteRule, batchDeleteRules,
  getCountries, getProductTypes, exportExcel, importExcel
} from '../api/index.js'

const rules = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const selectedIds = ref([])
const searchQuery = ref('')
const filterCountry = ref('')
const filterProductType = ref('')
const countries = ref([])
const productTypes = ref([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref(null)

const defaultForm = {
  country: '',
  productType: '',
  productGrade: '',
  productPriceMin: 0,
  productPriceMax: 0,
  lengthUnit: 'cm',
  weightUnit: 'g',
  lengthMin: 0,
  lengthMax: 0,
  widthMin: 0,
  widthMax: 0,
  heightMin: 0,
  heightMax: 0,
  weightMin: 0,
  weightMax: 0,
  price: 0,
  currency: 'USD',
  remark: ''
}

const form = ref({ ...defaultForm })

const formRules = {
  country: [{ required: true, message: '请选择国家', trigger: 'change' }],
  productType: [{ required: true, message: '请选择商品类型', trigger: 'change' }],
    productGrade: [{ required: true, message: '请输入产品等级', trigger: 'blur' }],
    productPriceMin: [{ required: true, message: '请输入商品价格最小值', trigger: 'blur' }],
    productPriceMax: [{ required: true, message: '请输入商品价格最大值', trigger: 'blur' }, { validator: (rule, value) => value >= form.value.productPriceMin, message: '最大值必须大于或等于最小值', trigger: 'blur' }],
  lengthMin: [{ required: true, message: '请输入长度最小值', trigger: 'blur' }],
  lengthMax: [
    { required: true, message: '请输入长度最大值', trigger: 'blur' },
    { validator: (rule, value) => value >= form.value.lengthMin, message: '必须大于最小值', trigger: 'blur' }
  ],
  widthMin: [{ required: true, message: '请输入宽度最小值', trigger: 'blur' }],
  widthMax: [
    { required: true, message: '请输入宽度最大值', trigger: 'blur' },
    { validator: (rule, value) => value >= form.value.widthMin, message: '必须大于最小值', trigger: 'blur' }
  ],
  heightMin: [{ required: true, message: '请输入高度最小值', trigger: 'blur' }],
  heightMax: [
    { required: true, message: '请输入高度最大值', trigger: 'blur' },
    { validator: (rule, value) => value >= form.value.heightMin, message: '必须大于最小值', trigger: 'blur' }
  ],
  weightMin: [{ required: true, message: '请输入重量最小值', trigger: 'blur' }],
  weightMax: [
    { required: true, message: '请输入重量最大值', trigger: 'blur' },
    { validator: (rule, value) => value >= form.value.weightMin, message: '必须大于最小值', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', message: '价格必须为数字', trigger: 'blur' }
  ],
  currency: [{ required: true, message: '请选择币种', trigger: 'change' }]
}

async function fetchRules() {
  loading.value = true
  try {
    const res = await getRules({
      page: page.value,
      page_size: pageSize.value,
      country: filterCountry.value || undefined,
      product_type: filterProductType.value || undefined,
      search: searchQuery.value || undefined
    })
    rules.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function handleCountryChange(country) {
  const found = countries.value.find(c => c.name === country)
  if (found) {
    form.value.currency = found.currency
  }
}

async function loadOptions() {
  try {
    const [cRes, tRes] = await Promise.all([getCountries(), getProductTypes()])
    countries.value = cRes.data
    productTypes.value = tRes.data
  } catch (e) {
    console.error(e)
  }
}

function resetFilters() {
  searchQuery.value = ''
  filterCountry.value = ''
  filterProductType.value = ''
  page.value = 1
  fetchRules()
}

function handleSelectionChange(rows) {
  selectedIds.value = rows.map(r => r.id)
}

function openAddDialog() {
  isEditing.value = false
  editingId.value = null
  form.value = { ...defaultForm }
  dialogVisible.value = true
}

function openEditDialog(row) {
  isEditing.value = true
  editingId.value = row.id
  form.value = {
    country: row.country,
    productType: row.productType,
    productGrade: row.productGrade,
    productPriceMin: row.productPriceMin,
    productPriceMax: row.productPriceMax,
    lengthUnit: row.lengthUnit,
    weightUnit: row.weightUnit,
    lengthMin: row.lengthMin,
    lengthMax: row.lengthMax,
    widthMin: row.widthMin,
    widthMax: row.widthMax,
    heightMin: row.heightMin,
    heightMax: row.heightMax,
    weightMin: row.weightMin,
    weightMax: row.weightMax,
    price: row.price,
    currency: row.currency,
    remark: row.remark
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const payload = { ...form.value }
    if (isEditing.value) {
      await updateRule(editingId.value, payload)
      ElMessage.success('规则更新成功')
    } else {
      await createRule(payload)
      ElMessage.success('规则创建成功')
    }
    dialogVisible.value = false
    fetchRules()
  } catch (e) {
    if (e?.detail?.message && e?.detail?.conflict) {
      try {
        await ElMessageBox.confirm(
          `与规则 #${e.detail.conflict.id} 冲突 (${e.detail.conflict.country}, ${e.detail.conflict.productType})，是否继续保存？`,
          '规则区间重叠',
          { confirmButtonText: '继续保存', cancelButtonText: '取消', type: 'warning' }
        )
        const payload = { ...form.value, force: true }
        if (isEditing.value) {
          await updateRule(editingId.value, payload)
        } else {
          await createRule(payload)
        }
        ElMessage.success('规则保存成功')
        dialogVisible.value = false
        fetchRules()
      } catch (confirmErr) {
        // User cancelled
      }
    } else {
      console.error(e)
    }
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id) {
  try {
    await deleteRule(id)
    ElMessage.success('规则删除成功')
    fetchRules()
  } catch (e) {
    console.error(e)
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectedIds.value.length} 条规则？`, '确认删除', { type: 'warning' })
    await batchDeleteRules(selectedIds.value)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchRules()
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

async function handleExport() {
  try {
    const res = await exportExcel()
    const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'shipping_rules.xlsx'
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    console.error(e)
  }
}

async function handleImport(file) {
  try {
    const res = await importExcel(file)
    ElMessage.success(res.data.message)
    fetchRules()
    return false
  } catch (e) {
    console.error(e)
    return false
  }
}

onMounted(() => {
  fetchRules()
  loadOptions()
})
</script>

<style scoped>
.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}
</style>
