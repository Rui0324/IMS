<template>
  <div class="page">
    <el-card shadow="hover" class="card">
      <div class="card-header">
        <div class="title">审计日志</div>
        <div class="sub">记录登录、创建、更新等关键动作</div>
      </div>
      <el-form :inline="true" :model="filters" class="filters">
        <el-form-item label="用户">
          <el-input v-model="filters.user" placeholder="用户名" clearable />
        </el-form-item>
        <el-form-item label="路径">
          <el-input v-model="filters.path" placeholder="/api/..." clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="load">查询</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="logs" stripe border v-loading="loading">
        <el-table-column prop="user_username" label="用户" width="140" />
        <el-table-column prop="path" label="路径" min-width="200" show-overflow-tooltip />
        <el-table-column prop="method" label="方法" width="90" />
        <el-table-column prop="status_code" label="状态" width="90" />
        <el-table-column prop="duration_ms" label="耗时(ms)" width="110" />
        <el-table-column prop="created_at" label="时间" min-width="160" />
      </el-table>
      <div class="pager">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="pager.page"
          :page-size="pager.pageSize"
          :total="pager.total"
          @current-change="onPage"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../api'

const logs = ref([])
const loading = ref(false)
const pager = reactive({ page: 1, pageSize: 10, total: 0 })
const filters = reactive({ user: '', path: '' })

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/admin/logs/', {
      params: { page: pager.page, pageSize: pager.pageSize, user: filters.user || undefined, path: filters.path || undefined }
    })
    logs.value = data?.list || data || []
    pager.total = data?.total || 0
  } finally {
    loading.value = false
  }
}

const reset = () => {
  filters.user = ''
  filters.path = ''
  pager.page = 1
  load()
}

const onPage = (page) => {
  pager.page = page
  load()
}

onMounted(load)
</script>

<style scoped>
.page {
  padding: 24px;
}
.card {
  border-radius: 12px;
}
.card-header {
  margin-bottom: 12px;
}
.title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2d3d;
}
.sub {
  color: #667185;
  font-size: 13px;
  margin-top: 4px;
}
.filters {
  margin-bottom: 12px;
}
.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}
@media (max-width: 768px) {
  .page {
    padding: 16px;
  }
}
</style>
