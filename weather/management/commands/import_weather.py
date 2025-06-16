# weather/management/commands/import_weather.py
import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from weather.models import WeatherRecord
from django.conf import settings

class Command(BaseCommand):
    help = 'Import weather data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        # Full path (in case relative path is given)
        if not os.path.isabs(csv_file_path):
            csv_file_path = os.path.join(settings.BASE_DIR, csv_file_path)

        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file_path}"))
            return

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                WeatherRecord.objects.create(
                    date=datetime.strptime(row['date'], '%Y-%m-%d'),
                    location=row['location'],
                    hour=row['hour'],
                    cuaca=row['cuaca'],
                    temperature=float(row['temperature']),
                    humidity=float(row['humidity']),
                    wind_speed=float(row['wind_speed'])
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} records from {csv_file_path}'))
