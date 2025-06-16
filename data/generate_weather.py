import pandas as pd
import numpy as np
from datetime import timedelta
import random
import datetime

def generate_weather_data(filename='weathers.csv', total_rows=2000):
    # Jumlah jam per hari (1..23)
    hours_per_day = 23
    
    # Hitung jumlah hari yang dibutuhkan supaya total_rows terpenuhi
    total_days = total_rows // hours_per_day
    if total_rows % hours_per_day != 0:
        total_days += 1
    
    # Mulai tanggal hari ini
    # start_date = datetime.today().date()
    start_date =  datetime.date(2025, 5, 1)
    
    # List untuk simpan data
    data = []
    
    cuaca_choices = ['Clear', 'Cloudy', 'Rain']
    locations = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Yogyakarta']
    
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        for hour in range(1, hours_per_day + 1):
            if len(data) >= total_rows:
                break
            
            temperature = round(random.uniform(20, 35), 1)  # suhu 20-35 °C
            cuaca = random.choice(cuaca_choices)
            humidity = random.randint(40, 90)  # kelembapan 40-90%
            wind_speed = round(random.uniform(0, 15), 1)  # kecepatan angin 0-15 km/h
            location = random.choice(locations)
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'hour': hour,
                'temperature': temperature,
                'cuaca': cuaca,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'location': location
            })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"File '{filename}' berhasil dibuat dengan {len(df)} baris data.")

if __name__ == "__main__":
    generate_weather_data()
