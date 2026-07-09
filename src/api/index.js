import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

request.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const detail = error.response.data
      if (error.response.status === 409) {
        return Promise.reject(detail)
      }
      var msg = detail?.detail?.message || (typeof detail?.detail==='string'?detail?.detail:Array.isArray(detail?.detail)?detail.detail[0]?.msg:null) || detail?.message || '请求失败'; ElMessage.error(msg)
    } else {
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export function getRules(params) {
  return request.get('/rules', { params })
}

export function createRule(data) {
  return request.post('/rules', data)
}

export function updateRule(id, data) {
  return request.put(`/rules/${id}`, data)
}

export function deleteRule(id) {
  return request.delete(`/rules/${id}`)
}

export function batchDeleteRules(ids) {
  return request.post('/rules/batch-delete', ids)
}

export function queryPrice(data) {
  return request.post('/query', data)
}

export function getCountries() {
  return request.get('/countries')
}

export function createCountry(data) {
  return request.post('/countries', data)
}

export function updateCountry(id, data) {
  return request.put(`/countries/${id}`, data)
}

export function deleteCountry(id) {
  return request.delete(`/countries/${id}`)
}

export function getProductTypes() {
  return request.get('/product-types')
}

export function createProductType(data) {
  return request.post('/product-types', data)
}

export function updateProductType(id, data) {
  return request.put(`/product-types/${id}`, data)
}

export function deleteProductType(id) {
  return request.delete(`/product-types/${id}`)
}

export function exportExcel() {
  return request.get('/export-excel', { responseType: 'blob' })
}

export function importExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/import-excel', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export default request
