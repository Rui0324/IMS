<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-position="top"
    class="login-form"
    @keyup.enter.prevent="handleSubmit"
  >
    <el-form-item label="用户名" prop="username">
      <el-input
        v-model="form.username"
        :prefix-icon="User"
        size="large"
        autocomplete="username"
        placeholder="请输入用户名"
      />
    </el-form-item>

    <el-form-item label="密码" prop="password">
      <el-input
        v-model="form.password"
        :type="passwordVisible ? 'text' : 'password'"
        :prefix-icon="Lock"
        size="large"
        autocomplete="current-password"
        placeholder="请输入密码"
      >
        <template #suffix>
          <el-icon class="toggle" @click="togglePassword">
            <component :is="passwordVisible ? View : Hide" />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>

    <div class="form-extras">
      <el-checkbox v-model="form.remember">记住我</el-checkbox>
      <el-link type="primary" :underline="false" @click="onForgot">忘记密码？</el-link>
    </div>

    <el-button type="primary" size="large" class="submit" :loading="loading" @click="handleSubmit">
      登录
    </el-button>
  </el-form>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const formRef = ref()
const usernameKey = 'ims-remember-username'

const form = reactive({
  username: localStorage.getItem(usernameKey) || '',
  password: '',
  remember: !!localStorage.getItem(usernameKey)
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const loading = ref(false)
const passwordVisible = ref(false)
const emit = defineEmits(['success'])

const persistRemembered = () => {
  if (form.remember) {
    localStorage.setItem(usernameKey, form.username)
  } else {
    localStorage.removeItem(usernameKey)
  }
}

const handleSubmit = () => {
  if (!formRef.value) return
  formRef.value.validate(async valid => {
    if (!valid) return
    loading.value = true
    try {
      await auth.login(form.username, form.password)
      persistRemembered()
      emit('success', auth.user)
    } catch (error) {
      const message = error?.response?.data?.msg || error?.message || '登录失败，请检查用户名或密码'
      ElMessage.error(message)
    } finally {
      loading.value = false
    }
  })
}

const togglePassword = () => {
  passwordVisible.value = !passwordVisible.value
}

const onForgot = () => {
  ElMessage.info('忘记密码功能即将上线')
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.el-form-item {
  margin-bottom: 8px;
}

.el-input__wrapper {
  border-radius: 10px;
}

.form-extras {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  margin-bottom: 4px;
}

.submit {
  width: 100%;
  margin-top: 6px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.toggle {
  cursor: pointer;
  color: var(--el-text-color-regular);
  transition: color 0.2s ease;
}

.toggle:hover {
  color: var(--el-color-primary);
}
</style>
