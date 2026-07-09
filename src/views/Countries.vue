<template>
  <div class="countries-page">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>国家管理</span>
          <el-button type="primary" size="small" @click="openDialog()">
            <el-icon><Plus /></el-icon>新增国家
          </el-button>
        </div>
      </template>

      <el-table :data="countries" stripe border v-loading="loading">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="name" label="国家名称" min-width="140" />
        <el-table-column prop="currency" label="币种" width="100" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确认删除该国家？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEditing ? '编辑国家' : '新增国家'" width="400px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入国家名称" />
        </el-form-item>
        <el-form-item label="币种" prop="currency">
          <el-input v-model="form.currency" placeholder="请输入币种，如 USD" />

        </el-form-item>
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
import { ElMessage } from 'element-plus'
import { getCountries, createCountry, updateCountry, deleteCountry } from '../api/index.js'

const countries = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref(null)
const form = ref({ name: '', currency: 'USD' })
const formRules = { name: [{ required: true, message: '请输入国家名称', trigger: 'blur' }],
    currency: [{ required: true, message: '请选择币种', trigger: 'change' }] }

async function fetchData() {
  loading.value = true
  try {
    const res = await getCountries()
    countries.value = res.data
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function openDialog(row) {
  if (row) {
    isEditing.value = true
    editingId.value = row.id
    form.value = { name: row.name, currency: row.currency }
  } else {
    isEditing.value = false
    editingId.value = null
    form.value = { name: '', currency: 'USD' }
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isEditing.value) {
      await updateCountry(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await createCountry(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (e) { console.error(e) }
  finally { submitting.value = false }
}

async function handleDelete(id) {
  try {
    await deleteCountry(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (e) { console.error(e) }
}

onMounted(fetchData)
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
