# log_dashboard/management/commands/delete_old_logs.py

from django.core.management.base import BaseCommand
from log_dashboard.models import UserActivityLog
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Hapus log yang lebih dari 30 hari'

    def handle(self, *args, **kwargs):
        batas_waktu = timezone.now() - timedelta(days=5)
        deleted, _ = UserActivityLog.objects.filter(timestamp__lt=batas_waktu).delete()
        self.stdout.write(f'{deleted} log dihapus.')
