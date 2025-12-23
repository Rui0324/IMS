from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from .models import StudentInfo
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == User.Roles.ADMIN:
            return StudentInfo.objects.all()
        return StudentInfo.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put'], url_path='me')
    def me(self, request):
        obj, _ = StudentInfo.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            return Response(StudentSerializer(obj).data)
        serializer = StudentSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
