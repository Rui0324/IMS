import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import StudentLayout from '../layout/StudentLayout.vue'
import TeacherLayout from '../layout/TeacherLayout.vue'
import AdminLayout from '../layout/AdminLayout.vue'
import Profile from '../views/student/Profile.vue'
import ProjectSubmit from '../views/student/ProjectSubmit.vue'
import Achievements from '../views/student/Achievements.vue'
import AIRecommend from '../views/student/AIRecommend.vue'
import StudentScores from '../views/student/Scores.vue'
import ReviewScores from '../views/teacher/ReviewScores.vue'
import AIQA from '../views/teacher/AIQA.vue'
import UserManage from '../views/admin/UserManage.vue'
import Permission from '../views/admin/Permission.vue'
import AuditLogs from '../views/admin/AuditLogs.vue'
import Dashboard from '../views/admin/Dashboard.vue'

const routes = [
  { path: '/login', component: Login },
  {
    path: '/student',
    component: StudentLayout,
    children: [
      { path: '', component: Profile },
      { path: 'project', component: ProjectSubmit },
      { path: 'achievements', component: Achievements },
      { path: 'scores', component: StudentScores },
      { path: 'ai', component: AIRecommend }
    ]
  },
  {
    path: '/teacher',
    component: TeacherLayout,
    children: [
      { path: '', component: ReviewScores },
      { path: 'ai', component: AIQA }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', component: Dashboard },
      { path: 'users', component: UserManage },
      { path: 'permissions', component: Permission },
      { path: 'logs', component: AuditLogs }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.path === '/login') return next()
  if (!auth.token) return next('/login')
  const role = auth.user?.role
  if (to.path.startsWith('/admin') && role !== 'admin') return next('/login')
  if (to.path.startsWith('/teacher') && role === 'student') return next('/login')
  if (to.path.startsWith('/student') && role !== 'student') return next('/login')
  next()
})

export default router
