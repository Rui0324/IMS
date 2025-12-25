<template>
  <div class="page">
    <el-card class="card" shadow="hover">
      <div class="card-header">
        <div class="title">个人信息</div>
        <div class="sub">完善基础信息便于教师评估与联系</div>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" status-icon class="profile-form">
        <el-form-item label="专业" prop="major">
          <el-input v-model="form.major" placeholder="如：计算机科学与技术" />
        </el-form-item>
        <el-form-item label="技能" prop="skills">
          <el-input v-model="form.skills" placeholder="如：Python、数据分析" />
        </el-form-item>
        <el-form-item label="兴趣方向" prop="interests">
          <el-input v-model="form.interests" placeholder="如：Web 开发、可视化" />
        </el-form-item>
        <el-form-item label="个人简介" prop="bio">
          <el-input v-model="form.bio" type="textarea" :rows="3" placeholder="简单介绍您的经历与兴趣" />
        </el-form-item>
        <div class="actions">
          <el-button type="primary" :loading="saving" @click="save">保存</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '../../api'

const formRef = ref()
const form = reactive({ major: '', skills: '', interests: '', bio: '' })
const rules = {
  major: [{ required: true, message: '请输入专业', trigger: 'blur' }],
  skills: [{ required: true, message: '请输入技能', trigger: 'blur' }],
  interests: [{ required: true, message: '请输入兴趣方向', trigger: 'blur' }]
}
const saving = ref(false)

const load = async () => {
  const { data } = await api.get('/students/me')
  Object.assign(form, data || {})
}

const save = () => {
  if (!formRef.value) return
  formRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      await api.put('/students/me', form)
      ElMessage.success('保存成功')
    } finally {
      saving.value = false
    }
  })
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
.profile-form {
  max-width: 720px;
}
.actions {
  margin-left: 120px;
}
@media (max-width: 768px) {
  .page {
    padding: 16px;
  }
  .profile-form {
    max-width: 100%;
  }
  .actions {
    margin-left: 0;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
