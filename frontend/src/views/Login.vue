<template>
  <div class="login-page">
    <div class="background"></div>
    <div class="login-shell">
      <div class="brand">
        <div class="logo">深蓝双创</div>
        <div class="subtitle">AI · 安全 · 可视化 校园创新创业平台</div>
      </div>
      <el-card class="login-card" shadow="hover">
        <div class="card-header">
          <div class="card-title">欢迎登录</div>
          <div class="card-desc">请使用校园账号登录，体验智能创新空间</div>
        </div>
        <LoginForm @success="onSuccess" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '../components/auth/LoginForm.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const onSuccess = user => {
  const role = user?.role
  if (role === 'admin') router.push('/admin')
  else if (role === 'teacher') router.push('/teacher')
  else router.push('/student')
}
</script>

<style scoped>
:global(body) {
  margin: 0;
  background: linear-gradient(135deg, #f5f7fb 0%, #eef1f7 40%, #e6ecfb 100%);
  font-family: 'PingFang SC', 'Inter', system-ui, -apple-system, sans-serif;
}

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 24px;
}

.background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 20%, rgba(64, 158, 255, 0.18), transparent 28%),
    radial-gradient(circle at 80% 0%, rgba(64, 158, 255, 0.12), transparent 30%),
    radial-gradient(circle at 50% 80%, rgba(64, 158, 255, 0.12), transparent 32%);
  filter: blur(0px);
  z-index: 0;
}

.login-shell {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
  max-width: 520px;
  width: min(92vw, 520px);
}

.brand {
  text-align: center;
  color: #1f2d3d;
}

.logo {
  font-size: clamp(22px, 4vw, 28px);
  font-weight: 700;
  letter-spacing: 0.6px;
}

.subtitle {
  margin-top: 6px;
  font-size: clamp(13px, 3vw, 15px);
  color: #5c6b7a;
}

.login-card {
  border-radius: 14px;
  box-shadow: 0 18px 40px rgba(31, 45, 61, 0.08);
  border: 1px solid rgba(64, 158, 255, 0.08);
  backdrop-filter: blur(2px);
}

.card-header {
  margin-bottom: 12px;
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2d3d;
}

.card-desc {
  margin-top: 6px;
  color: #718096;
  font-size: 13px;
}

@media (max-width: 540px) {
  .login-shell {
    width: 100%;
  }

  .login-card {
    padding: 16px 14px;
  }

  .card-title {
    font-size: 18px;
  }

  .card-desc {
    font-size: 12px;
  }
}
</style>
