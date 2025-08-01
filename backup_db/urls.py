from django.urls import path
from .views import backup_database, download_backup, index, delete_backup

# app_name = 'backup_db'
urlpatterns = [
    path('', index, name='backup_db'),  # ← halaman tombol
    path('proses/', backup_database, name='backup_database'),  # ← POST saja
    # path('', backup_database, name='backup_database'),
    path('unduh/<str:filename>/', download_backup, name='download_backup'),
    path('hapus/<str:filename>/', delete_backup, name='delete_backup'),
]
