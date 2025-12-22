from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from apps.accounts.views import AuthViewSet, UserAdminViewSet
from apps.students.views import StudentViewSet
from apps.projects.views import ProjectViewSet
from apps.scores.views import ScoreViewSet
from apps.messages.views import MessageViewSet
from apps.auditlog.views import AuditLogViewSet, StatsView
from apps.ai.views import AIViewSet

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'scores', ScoreViewSet, basename='scores')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')
router.register(r'admin/logs', AuditLogViewSet, basename='admin-logs')
router.register(r'ai', AIViewSet, basename='ai')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('api/auth/register', AuthViewSet.as_view({'post': 'register'})),
    path('api/auth/login', AuthViewSet.as_view({'post': 'login'})),
    path('api/auth/refresh', AuthViewSet.as_view({'post': 'refresh'})),
    path('api/auth/me', AuthViewSet.as_view({'get': 'me'})),
    path('api/', include(router.urls)),
    path('api/admin/stats/', StatsView.as_view(), name='admin-stats'),
]

urlpatterns += [
    path('api/projects/<int:pk>/upload', ProjectViewSet.as_view({'post': 'upload'}), name='project-upload'),
]
