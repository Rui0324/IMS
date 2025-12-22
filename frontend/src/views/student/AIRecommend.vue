<template>
  <div class="p-4">
    <el-input type="textarea" v-model="input" placeholder="输入兴趣或方向" />
    <el-button class="mt-2" type="primary" @click="ask">获取推荐</el-button>
    <el-timeline>
      <el-timeline-item v-for="item in list" :key="item.title" :timestamp="item.title">
        {{ item.desc }}
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../../api'

const input = ref('')
const list = ref([])

const ask = async () => {
  const { data } = await api.post('/ai/recommend', { profile: input.value })
  list.value = data.recommendations
}
</script>
