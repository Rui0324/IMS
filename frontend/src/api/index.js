import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export const api = axios.create({
  baseURL: '/api'
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth?.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

api.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const auth = useAuthStore()
    if (error.response?.status === 401 && auth.refresh) {
      try {
        const { data } = await axios.post('/api/auth/refresh', { refresh: auth.refresh })
        auth.token = data.access
        localStorage.setItem('token', data.access)
        error.config.headers.Authorization = `Bearer ${data.access}`
        return api.request(error.config)
      } catch (e) {
        auth.logout()
        window.location = '/login'
      }
    }
    return Promise.reject(error)
  }
)
