from django.shortcuts import render
from .models import UserActivityLog
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
import csv
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def user_log_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("Anda tidak memiliki akses ke halaman ini.")
    query = request.GET.get('q', '')
    method = request.GET.get('method', '')
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


    if method:
        logs = logs.filter(method__iexact=method)
    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)
    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)
    paginator = Paginator(logs, int(per_page))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    # Ambil jumlah hari dari querystring, default 30
    try:
        days = int(request.GET.get('days_to_delete', 30))
    except ValueError:
        days = 30

    batas_waktu = timezone.now() - timedelta(days=days)
    log_akan_dihapus = UserActivityLog.objects.filter(timestamp__lt=batas_waktu).count()
    
    per_page_options = [5, 10, 20, 50, 100]
    method_options = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    return render(request, 'log_dashboard/index.html', {
        'page_obj': page_obj,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'per_page': per_page,
        'per_page_options': per_page_options,  # ← kirim ke template
        'log_akan_dihapus': log_akan_dihapus,
        'days': days,
        'method_options': method_options,
        'method': method,
    })

@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
def hapus_log_lama(request):
    try:
        days = int(request.POST.get('days_to_delete', 30))
    except ValueError:
        days = 30

    batas_waktu = timezone.now() - timedelta(days=days)
    deleted, _ = UserActivityLog.objects.filter(timestamp__lt=batas_waktu).delete()
    messages.success(request, f'{deleted} log yang lebih dari {days} hari telah dihapus.')
    return redirect('log_dashboard')

@user_passes_test(is_staff_user, login_url='dashboard')
@login_required
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
