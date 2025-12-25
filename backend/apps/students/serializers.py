from rest_framework import serializers

from .models import StudentInfo


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = StudentInfo
        fields = ['id', 'user_id', 'username', 'email', 'major', 'bio', 'skills', 'interests']

    def create(self, validated_data):
        user = self.context['request'].user
        return StudentInfo.objects.create(user=user, **validated_data)
