from rest_framework import serializers

from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    project_title = serializers.ReadOnlyField(source='project.title')
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')
    student_username = serializers.ReadOnlyField(source='project.owner.username')

    class Meta:
        model = Score
        fields = [
            'id',
            'project',
            'project_title',
            'student_username',
            'reviewer',
            'reviewer_username',
            'score',
            'comment',
            'status',
            'created_at',
        ]
        read_only_fields = ['reviewer', 'created_at']
