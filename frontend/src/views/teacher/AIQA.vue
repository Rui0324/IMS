<template>
  <div class="p-4">
    <el-input type="textarea" v-model="question" placeholder="输入问题" />
    <el-button class="mt-2" type="primary" @click="ask">提问</el-button>
    <el-card class="mt-2">{{ answer }}</el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../../api'

const question = ref('')
const answer = ref('')

const ask = async () => {
  const { data } = await api.post('/ai/qa', { question: question.value })
  answer.value = data.answer
}
</script>
