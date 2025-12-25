<template>
  <div class="page">
    <el-card shadow="hover" class="card">
      <div class="card-header">
        <div class="title">我的成绩</div>
        <div class="sub">查看教师评审结果与状态</div>
      </div>
      <el-table :data="scores" stripe border v-loading="loading">
        <el-table-column prop="project_title" label="项目" min-width="160" />
        <el-table-column prop="score" label="分数" width="90" />
        <el-table-column prop="comment" label="评语" min-width="200" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reviewer_username" label="评审教师" width="140" />
        <el-table-column prop="created_at" label="时间" min-width="160" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../../api'

const scores = ref([])
const loading = ref(false)

const statusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'info'
}
const statusLabel = (status) => {
  if (status === 'approved') return '已通过'
  if (status === 'rejected') return '已驳回'
  return '待审核'
}

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/scores/', { params: { pageSize: 50 } })
    scores.value = data?.list || data || []
  } finally {
    loading.value = false
  }
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
@media (max-width: 768px) {
  .page {
    padding: 16px;
  }
}
</style>
