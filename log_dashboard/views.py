from django.shortcuts import render
from .models import UserActivityLog
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import csv
import datetime

def user_log_dashboard(request):
    query = request.GET.get('q', '')
    logs = UserActivityLog.objects.select_related('user').order_by('-timestamp')

    if query:
        logs = logs.filter(
            Q(user__username__icontains=query) |
            Q(path__icontains=query) |
            Q(ip_address__icontains=query)
        )

    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'log_dashboard/index.html', {
        'page_obj': page_obj,
        'query': query
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
