import { defineStore } from 'pinia'
import { api } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({ token: localStorage.getItem('token') || '', refresh: localStorage.getItem('refresh') || '', user: JSON.parse(localStorage.getItem('user') || 'null') }),
  actions: {
    async login(username, password) {
      const { data } = await api.post('/auth/login', { username, password })
      this.token = data.access
      this.refresh = data.refresh
      this.user = data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('refresh', this.refresh)
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    logout() {
      this.token = ''
      this.refresh = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    }
  }
})
