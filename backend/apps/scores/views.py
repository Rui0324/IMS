from rest_framework import permissions, viewsets

from apps.accounts.models import User
from .models import Score
from .serializers import ScoreSerializer


class ScorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in [User.Roles.TEACHER, User.Roles.ADMIN]


class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [ScorePermission]

    def get_queryset(self):
        if self.request.user.role in [User.Roles.TEACHER, User.Roles.ADMIN]:
            return Score.objects.all()
        return Score.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
