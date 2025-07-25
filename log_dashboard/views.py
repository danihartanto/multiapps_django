from django.shortcuts import render
from .models import UserActivityLog
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
import csv
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user)
@login_required
def user_log_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("Anda tidak memiliki akses ke halaman ini.")
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    per_page = request.GET.get('per_page', '20')  # default 20

    logs = UserActivityLog.objects.select_related('user').order_by('-timestamp')

    if query:
        logs = logs.filter(
            Q(user__username__icontains=query) |
            Q(path__icontains=query) |
            Q(ip_address__icontains=query)
        )

    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)
    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)

    paginator = Paginator(logs, int(per_page))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [5, 10, 20, 50, 100]
    return render(request, 'log_dashboard/index.html', {
        'page_obj': page_obj,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'per_page': per_page,
        'per_page_options': per_page_options,  # ← kirim ke template
    })

def export_user_logs(request):
    date_now = datetime.datetime.now()
    formatted_date = date_now.strftime("%Y_%m_%d %H_%M_%S")
    print(formatted_date)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_logs_"'+formatted_date+'".csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Username', 'Method', 'Path', 'IP Address'])

    logs = UserActivityLog.objects.select_related('user').order_by('-timestamp')
    for log in logs:
        writer.writerow([
            log.timestamp,
            log.user.username,
            log.method,
            log.path,
            log.ip_address
        ])

    return response
