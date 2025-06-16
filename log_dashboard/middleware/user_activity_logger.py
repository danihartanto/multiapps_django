from log_dashboard.models import UserActivityLog
from django.utils.deprecation import MiddlewareMixin

class UserActivityLoggerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.path.startswith(('/static/', '/admin/')):
            ip = self.get_client_ip(request)
            UserActivityLog.objects.create(
                user=request.user,
                method=request.method,
                path=request.path,
                ip_address=ip
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
