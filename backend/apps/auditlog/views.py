from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.views import IsAdmin
from .models import Log
from .serializers import LogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user')
        path = self.request.query_params.get('path')
        if user:
            queryset = queryset.filter(user__username=user)
        if path:
            queryset = queryset.filter(path__icontains=path)
        return queryset


class StatsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from apps.accounts.models import User
        from apps.projects.models import Project
        from apps.scores.models import Score

        now = timezone.now()
        last_week = now - timedelta(days=7)
        trend = (
            Project.objects.filter(created_at__gte=last_week)
            .extra({'day': "date(created_at)"})
            .values('day')
            .order_by('day')
            .annotate(count=Count('id'))
        )
        data = {
            'users': User.objects.count(),
            'projects': Project.objects.count(),
            'approved_rate': Score.objects.filter(status='approved').count(),
            'trend': list(trend),
        }
        return Response(data)
