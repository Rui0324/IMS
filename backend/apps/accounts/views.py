from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action

from config.api import ApiResponseMixin, api_response
from .serializers import LoginSerializer, RefreshSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Roles.ADMIN)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def register(self, request):
        # 仅管理员可创建，若系统无用户可用于初始化
        if User.objects.exists() and not (request.user.is_authenticated and request.user.role == User.Roles.ADMIN):
            return api_response(None, msg='forbidden', code=1003, status_code=status.HTTP_403_FORBIDDEN)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return api_response(UserSerializer(user).data, status_code=status.HTTP_201_CREATED)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(None, msg='Invalid username or password', code=1002, status_code=status.HTTP_401_UNAUTHORIZED)
        return api_response(serializer.validated_data)

    def refresh(self, request):
        serializer = RefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(None, msg='Invalid refresh token', code=1002, status_code=status.HTTP_401_UNAUTHORIZED)
        return api_response(serializer.validated_data)

    def me(self, request):
        return api_response(UserSerializer(request.user).data)


class UserAdminViewSet(ApiResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=['post'])
    def role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')
        if role not in dict(User.Roles.choices):
            return api_response(None, msg='invalid role', code=1001, status_code=status.HTTP_400_BAD_REQUEST)
        user.role = role
        user.save()
        return api_response(UserSerializer(user).data)
