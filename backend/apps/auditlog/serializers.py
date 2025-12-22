from rest_framework import serializers

from .models import Log


class LogSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Log
        fields = ['id', 'user', 'user_username', 'ip', 'path', 'method', 'status_code', 'duration_ms', 'summary', 'created_at']
