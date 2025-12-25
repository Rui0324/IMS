import os

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from .models import Project
from .serializers import ProjectSerializer


class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [User.Roles.TEACHER, User.Roles.ADMIN]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in [User.Roles.TEACHER, User.Roles.ADMIN]:
            return Project.objects.all()
        return Project.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def upload(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user and request.user.role == User.Roles.STUDENT:
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        file: UploadedFile = request.FILES.get('file')
        if not file:
            return Response({'detail': 'no file'}, status=status.HTTP_400_BAD_REQUEST)
        allowed = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.zip']
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed or file.size > 10 * 1024 * 1024:
            return Response({'detail': 'invalid file'}, status=status.HTTP_400_BAD_REQUEST)
        path = default_storage.save(f'projects/{file.name}', file)
        project.attachment = path
        project.save()
        return Response(ProjectSerializer(project).data)
