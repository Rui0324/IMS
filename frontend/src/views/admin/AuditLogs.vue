<template>
  <div class="p-4">
    <el-table :data="logs">
      <el-table-column prop="user_username" label="用户" />
      <el-table-column prop="path" label="路径" />
      <el-table-column prop="status_code" label="状态" />
      <el-table-column prop="duration_ms" label="耗时(ms)" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../../api'

const logs = ref([])

const load = async () => {
  const { data } = await api.get('/admin/logs/')
  logs.value = data
}

onMounted(load)
</script>
