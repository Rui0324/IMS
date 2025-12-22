from django.db import models
from rest_framework import permissions, viewsets

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(models.Q(recipient=user) | models.Q(role_target=user.role) | models.Q(sender=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
