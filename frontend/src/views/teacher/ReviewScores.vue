<template>
  <div class="p-4">
    <el-table :data="items">
      <el-table-column prop="project_title" label="项目" />
      <el-table-column prop="score" label="分数" />
      <el-table-column prop="status" label="状态" />
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../../api'

const items = ref([])

const load = async () => {
  const { data } = await api.get('/scores/')
  items.value = data
}

onMounted(load)
</script>
