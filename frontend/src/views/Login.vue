<template>
  <div class="login">
    <el-card class="box">
      <h2>深蓝双创 - 登录</h2>
      <el-form @submit.prevent="onSubmit" :model="form">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-button type="primary" @click="onSubmit" block>登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({ username: '', password: '' })

const onSubmit = async () => {
  await auth.login(form.username, form.password)
  const role = auth.user.role
  if (role === 'admin') router.push('/admin')
  else if (role === 'teacher') router.push('/teacher')
  else router.push('/student')
}
</script>

<style scoped>
.login { display: flex; justify-content: center; align-items: center; height: 100vh; }
.box { width: 360px; }
</style>
