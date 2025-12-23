<template>
  <div class="p-4">
    <el-row :gutter="20">
      <el-col :span="6"><el-card>用户数: {{ stats?.users || 0 }}</el-card></el-col>
      <el-col :span="6"><el-card>项目数: {{ stats?.projects || 0 }}</el-card></el-col>
      <el-col :span="6"><el-card>审核通过: {{ stats?.approved_rate || 0 }}</el-card></el-col>
    </el-row>
    <div ref="chart" style="height:300px;margin-top:20px;"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../stores/dashboard'

const store = useDashboardStore()
const chart = ref(null)

onMounted(async () => {
  await store.fetchStats()
  const instance = echarts.init(chart.value)
  instance.setOption({
    xAxis: { type: 'category', data: store.stats?.trend?.map((i) => i.day) || [] },
    yAxis: { type: 'value' },
    series: [
      { type: 'line', data: store.stats?.trend?.map((i) => i.count) || [] },
      { type: 'bar', data: store.stats?.trend?.map((i) => i.count) || [] },
      { type: 'pie', radius: 50, center: ['80%', '40%'], data: [
        { value: store.stats?.users || 0, name: '用户' },
        { value: store.stats?.projects || 0, name: '项目' }
      ] }
    ]
  })
})

const stats = store.stats
</script>
