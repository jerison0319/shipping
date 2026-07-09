<template>
  <div class="product-types-page">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>商品类型管理</span>
          <el-button type="primary" size="small" @click="openDialog()">
            <el-icon><Plus /></el-icon>新增商品类型
          </el-button>
        </div>
      </template>

      <el-table :data="productTypes" stripe border v-loading="loading">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="name" label="商品类型" min-width="200" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确认删除该商品类型？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEditing ? '编辑商品类型' : '新增商品类型'" width="400px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品类型名称" />
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
import { getProductTypes, createProductType, updateProductType, deleteProductType } from '../api/index.js'

const productTypes = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref(null)
const form = ref({ name: '' })
const formRules = { name: [{ required: true, message: '请输入商品类型名称', trigger: 'blur' }] }

async function fetchData() {
  loading.value = true
  try {
    const res = await getProductTypes()
    productTypes.value = res.data
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function openDialog(row) {
  if (row) {
    isEditing.value = true
    editingId.value = row.id
    form.value = { name: row.name }
  } else {
    isEditing.value = false
    editingId.value = null
    form.value = { name: '' }
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isEditing.value) {
      await updateProductType(editingId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await createProductType(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (e) { console.error(e) }
  finally { submitting.value = false }
}

async function handleDelete(id) {
  try {
    await deleteProductType(id)
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
