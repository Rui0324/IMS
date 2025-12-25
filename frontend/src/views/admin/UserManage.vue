<template>
  <div class="p-4">
    <el-form inline :model="form">
      <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
      <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="form.role" placeholder="选择角色">
          <el-option label="学生" value="student" />
          <el-option label="教师" value="teacher" />
          <el-option label="管理员" value="admin" />
        </el-select>
      </el-form-item>
      <el-button type="primary" @click="create">创建</el-button>
    </el-form>
    <el-table :data="users" class="mt-4">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { api } from '../../api'

const users = ref([])
const form = reactive({ username: '', email: '', role: 'student', password: '12345678' })

const load = async () => {
  const { data } = await api.get('/admin/users/')
  users.value = data
}

const create = async () => {
  await api.post('/admin/users/', form)
  await load()
}

onMounted(load)
</script>
