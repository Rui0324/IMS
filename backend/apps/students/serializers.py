from rest_framework import serializers

from .models import StudentInfo


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ['id', 'major', 'bio', 'skills', 'interests']

    def create(self, validated_data):
        user = self.context['request'].user
        return StudentInfo.objects.create(user=user, **validated_data)
