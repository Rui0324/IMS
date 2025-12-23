<template>
  <div class="p-4">
    <el-form :model="form">
      <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
      <el-form-item label="描述"><el-input type="textarea" v-model="form.description" /></el-form-item>
      <el-form-item label="方向"><el-input v-model="form.direction" /></el-form-item>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-form>
    <el-upload action="" :auto-upload="false" :on-change="onFileChange">
      <el-button>选择附件</el-button>
    </el-upload>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { api } from '../../api'

const form = reactive({ title: '', description: '', direction: '' })
let file = null

const submit = async () => {
  const { data } = await api.post('/projects/', form)
  if (file) {
    const fd = new FormData()
    fd.append('file', file)
    await api.post(`/projects/${data.id}/upload`, fd)
  }
}

const onFileChange = (uploadFile) => {
  file = uploadFile.raw
}
</script>
