import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export const api = axios.create({
  baseURL: '/api'
})

const unwrap = (resp) => {
  const payload = resp?.data
  const hasCode = payload && typeof payload === 'object' && Object.prototype.hasOwnProperty.call(payload, 'code')
  if (hasCode) {
    if (payload.code !== 0) {
      const error = new Error(payload.msg || '请求失败')
      error.response = { ...resp, data: payload }
      throw error
    }
    return payload.data
  }
  return payload
}

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth?.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

api.interceptors.response.use(
  (resp) => {
    try {
      return { ...resp, data: unwrap(resp) }
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async (error) => {
    const auth = useAuthStore()
    if (error.response?.status === 401 && auth.refresh) {
      try {
        const refreshResp = await axios.post('/api/auth/refresh', { refresh: auth.refresh })
        const refreshed = unwrap(refreshResp)
        auth.token = refreshed.access
        localStorage.setItem('token', refreshed.access)
        if (error.config) {
          error.config.headers.Authorization = `Bearer ${refreshed.access}`
          return api.request(error.config)
        }
      } catch (e) {
        auth.logout()
        window.location = '/login'
      }
    }
    return Promise.reject(error)
  }
)
