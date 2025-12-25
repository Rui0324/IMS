import time

from apps.auditlog.models import Log


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = (time.time() - start) * 1000
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
        Log.objects.create(
            user=user,
            ip=request.META.get('REMOTE_ADDR'),
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=duration,
            summary=response.reason_phrase or '',
        )
        return response
