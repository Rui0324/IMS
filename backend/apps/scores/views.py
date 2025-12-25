from rest_framework import permissions, viewsets

from config.api import ApiResponseMixin
from apps.accounts.models import User
from .models import Score
from .serializers import ScoreSerializer


class ScorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in [User.Roles.TEACHER, User.Roles.ADMIN]


class ScoreViewSet(ApiResponseMixin, viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [ScorePermission]

    def get_queryset(self):
        if self.request.user.role in [User.Roles.TEACHER, User.Roles.ADMIN]:
            return Score.objects.select_related('project', 'reviewer', 'project__owner').all()
        return Score.objects.select_related('project', 'reviewer', 'project__owner').filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
