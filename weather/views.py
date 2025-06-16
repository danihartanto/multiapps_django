from django.shortcuts import render
from django.db.models import Avg
from weather.models import WeatherRecord
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta, date
import datetime

def predict_temperature(temperatures):
    """
    Prediksi suhu besok berdasarkan rata-rata perubahan suhu harian.
    temperatures: list suhu berurutan berdasarkan waktu (ascending)
    """
    if len(temperatures) < 2:
        return None  # data tidak cukup

    # Hitung perubahan suhu harian (delta)
    deltas = []
    for i in range(1, len(temperatures)):
        delta = temperatures[i] - temperatures[i-1]
        deltas.append(delta)

    # Rata-rata perubahan suhu
    avg_delta = sum(deltas) / len(deltas)

    # Prediksi suhu besok = suhu hari terakhir + rata-rata delta
    predicted_temp = temperatures[-1] + avg_delta
    return round(predicted_temp, 2)

from collections import Counter

def predict_weather_condition(weather_conditions):
    """
    Prediksi cuaca kategori berdasarkan frekuensi kemunculan pada data terakhir.
    weather_conditions: list kategori cuaca berurutan (ascending waktu)
    """
    if not weather_conditions:
        return None

    # Ambil 7 hari terakhir (atau seluruh data jika kurang)
    recent_conditions = weather_conditions[-7:]

    # Hitung frekuensi masing-masing kondisi
    freq = Counter(recent_conditions)

    # Kategori yang paling sering muncul
    predicted_condition = freq.most_common(1)[0][0]
    return predicted_condition

def get_recent_weather_data(days=3):
    # today = date.today()
    # today = datetime.date(2025, 6, 7)
    today = datetime.date(2025, 7, 26)
    # print(d)
    besok = today + timedelta(1)
    last_date = today
    start_date = today - timedelta(days=days)

    records = WeatherRecord.objects.filter(date__gte=start_date).order_by('date', 'hour')

    timestamps_3days = [f"{rec.date.strftime('%Y-%m-%d')} {rec.hour:02d}:00" for rec in records]
    temperatures = [rec.temperature for rec in records]

    return timestamps_3days, temperatures, besok, last_date

def dashboard(request):
    qs = WeatherRecord.objects.order_by('-date')[:30]
    avg_temp = qs.aggregate(Avg('temperature'))['temperature__avg']
    records = list(qs)[::-1]  # balik urutannya supaya ascending


    records_data = WeatherRecord.objects.order_by('date')  # urut tanggal ascending

    # Siapkan data untuk chart (list tanggal & suhu)
    dates = [record.date.strftime('%Y-%m-%d') for record in records_data]
    temperatures = [record.temperature for record in records_data]
    
    # temperatures = [rec.temperature for rec in records]

    predicted_temp = predict_temperature(temperatures)
    if predicted_temp is None:
        prediction = "Data tidak cukup untuk prediksi"
    else:
        prediction = predicted_temp

    #prediksi jenis cuaca
    records_cuaca = WeatherRecord.objects.order_by('date')
    weather_conditions = [rec.cuaca for rec in records_cuaca]
    predicted_condition = predict_weather_condition(weather_conditions)
    if predicted_condition is None:
        condition_prediction = "Data tidak cukup untuk prediksi cuaca"
    else:
        condition_prediction = predicted_condition

    
    # untuk prediksi data
    # Siapkan data jika cukup banyak (minimal 2 hari)
    # if len(temperatures) < 2:
    #     prediction = "Data belum cukup"
    # else:
    #     # Gunakan indeks hari sebagai fitur (X), suhu sebagai target (y)
    #     X = np.array(range(len(temperatures))).reshape(-1, 1)
    #     y = np.array(temperatures)
        
    #     # Buat model regresi linear
    #     model = LinearRegression()
    #     model.fit(X, y)
        
    #     # Prediksi suhu untuk hari besok (index = len)
    #     next_day_index = len(temperatures)
    #     prediction = model.predict(np.array([[next_day_index]]))[0]
    #     prediction = round(prediction, 2)

    records_time = WeatherRecord.objects.order_by('date', 'hour')
    timestamps = [f"{rec.date.strftime('%Y-%m-%d')} {rec.hour:02d}:00" for rec in records_time]  
    timestamps_3days, temperatures_3days, besok, last_date = get_recent_weather_data(days=3)
    context = {
        'dates': dates,
        'timestamps': timestamps,
        'timestamps_3days': timestamps_3days,
        'temperatures_3days': temperatures_3days,
        'date_temp_list': zip(dates, temperatures),
        'temperatures': temperatures,
        'records': records,
        'avg_temp': avg_temp,
        'predicted_temp': prediction,
        'predicted_condition': condition_prediction,
        'besok' : besok,
        'last_date' : last_date
    }
    return render(request, 'weather/dashboard.html', context)
