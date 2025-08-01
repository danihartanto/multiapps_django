from django.urls import path
from .views import user_log_dashboard, export_user_logs, hapus_log_lama

urlpatterns = [
    path('', user_log_dashboard, name='log_dashboard'),
    path('logs/export/', export_user_logs, name='export_user_logs'),
    path('hapus_log_lama/', hapus_log_lama, name='hapus_log_lama'),
]
