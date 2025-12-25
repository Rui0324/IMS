<template>
  <div class="page">
    <el-card shadow="hover" class="card">
      <div class="card-header">
        <div class="title">成绩录入与审核</div>
        <div class="sub">录入评分并维护审核状态，遵循统一表单与表格规范</div>
      </div>
      <el-form :model="form" label-width="120px" class="form" @submit.prevent>
        <el-row :gutter="16">
          <el-col :md="8" :sm="12" :xs="24">
            <el-form-item label="项目 ID">
              <el-input v-model="form.project" type="number" placeholder="请输入项目 ID" />
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="12" :xs="24">
            <el-form-item label="分数">
              <el-input v-model="form.score" type="number" placeholder="0-100" />
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24" :xs="24">
            <el-form-item label="状态">
              <el-select v-model="form.status" class="full" placeholder="请选择">
                <el-option label="待审核" value="pending" />
                <el-option label="通过" value="approved" />
                <el-option label="驳回" value="rejected" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="评语">
              <el-input v-model="form.comment" type="textarea" :rows="2" placeholder="可选填写反馈" />
            </el-form-item>
          </el-col>
        </el-row>
        <div class="actions">
          <el-button type="primary" :loading="submitting" @click="createScore">提交评分</el-button>
          <el-button @click="reset">重置</el-button>
        </div>
      </el-form>
    </el-card>

    <el-card shadow="hover" class="card">
      <div class="card-header">
        <div class="title">评分记录</div>
      </div>
      <el-table :data="items" stripe border v-loading="loading">
        <el-table-column prop="project_title" label="项目" min-width="160" />
        <el-table-column prop="student_username" label="学生" width="120" />
        <el-table-column prop="score" label="分数" width="100">
          <template #default="{ row }">
            <el-input-number v-model="row.score" :min="0" :max="100" size="small" @change="updateRow(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="140">
          <template #default="{ row }">
            <el-select v-model="row.status" size="small" @change="updateRow(row)">
              <el-option label="待审核" value="pending" />
              <el-option label="通过" value="approved" />
              <el-option label="驳回" value="rejected" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="评语" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <el-input v-model="row.comment" size="small" @change="updateRow(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="reviewer_username" label="评审教师" width="140" />
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
import { ElMessage } from 'element-plus'
import { api } from '../../api'

const loading = ref(false)
const submitting = ref(false)
const items = ref([])
const pager = reactive({ page: 1, pageSize: 10, total: 0 })
const form = reactive({ project: '', score: '', status: 'pending', comment: '' })

const reset = () => {
  form.project = ''
  form.score = ''
  form.status = 'pending'
  form.comment = ''
}

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/scores/', { params: { page: pager.page, pageSize: pager.pageSize } })
    items.value = data?.list || data || []
    pager.total = data?.total || 0
  } finally {
    loading.value = false
  }
}

const createScore = async () => {
  if (!form.project || form.score === '') {
    ElMessage.warning('请填写项目 ID 和分数')
    return
  }
  submitting.value = true
  try {
    await api.post('/scores/', {
      project: Number(form.project),
      score: Number(form.score),
      status: form.status,
      comment: form.comment
    })
    ElMessage.success('提交成功')
    reset()
    await load()
  } finally {
    submitting.value = false
  }
}

const updateRow = async (row) => {
  await api.patch(`/scores/${row.id}/`, {
    score: row.score,
    status: row.status,
    comment: row.comment
  })
  ElMessage.success('已更新')
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
  display: flex;
  flex-direction: column;
  gap: 16px;
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
.form {
  margin-top: 8px;
}
.actions {
  display: flex;
  gap: 8px;
  margin-left: 120px;
}
.full {
  width: 100%;
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
  .actions {
    margin-left: 0;
    justify-content: flex-end;
  }
}
</style>
