<template>
  <div class="p-4">
    <el-form :model="form">
      <el-form-item label="专业">
        <el-input v-model="form.major" />
      </el-form-item>
      <el-form-item label="技能">
        <el-input v-model="form.skills" />
      </el-form-item>
      <el-form-item label="兴趣">
        <el-input v-model="form.interests" />
      </el-form-item>
      <el-button type="primary" @click="save">保存</el-button>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { api } from '../../api'

const form = reactive({ major: '', skills: '', interests: '' })

const load = async () => {
  const { data } = await api.get('/students/me')
  Object.assign(form, data || {})
}

const save = async () => {
  await api.put('/students/me', form)
}

onMounted(load)
</script>
