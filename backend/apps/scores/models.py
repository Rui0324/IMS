from django.conf import settings
from django.db import models

from apps.projects.models import Project


class Score(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='scores')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score {self.score} for {self.project.title}"
