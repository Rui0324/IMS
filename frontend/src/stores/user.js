import { defineStore } from 'pinia'
import { api } from '../api'

export const useUserStore = defineStore('user', {
  state: () => ({ profile: null }),
  actions: {
    async fetchMe() {
      const { data } = await api.get('/auth/me')
      this.profile = data
    }
  }
})
