import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../views/Layout.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页', icon: 'HomeFilled' }
      },
      {
        path: 'rules',
        name: 'Rules',
        component: () => import('../views/Rules.vue'),
        meta: { title: '配送规则管理', icon: 'List' }
      },
      {
        path: 'countries',
        name: 'Countries',
        component: () => import('../views/Countries.vue'),
        meta: { title: '国家管理', icon: 'Flag' }
      },
      {
        path: 'product-types',
        name: 'ProductTypes',
        component: () => import('../views/ProductTypes.vue'),
        meta: { title: '商品类型管理', icon: 'Goods' }
      },
      {
        path: 'price-query',
        name: 'PriceQuery',
        component: () => import('../views/PriceQuery.vue'),
        meta: { title: '价格查询', icon: 'Search' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
