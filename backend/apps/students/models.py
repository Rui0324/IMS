from django.conf import settings
from django.db import models


class StudentInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_info')
    major = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=200, blank=True)
    interests = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
