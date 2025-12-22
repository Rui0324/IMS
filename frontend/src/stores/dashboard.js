import { defineStore } from 'pinia'
import { api } from '../api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({ stats: null }),
  actions: {
    async fetchStats() {
      const { data } = await api.get('/admin/stats/')
      this.stats = data
    }
  }
})
