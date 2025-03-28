# -*- coding: utf-8 -*-
"""WeatherData.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NKaBYlo1cW_ZojFXth6eMzkn_o4jzxlB
"""

import requests
import csv
from datetime import datetime, timedelta

API_key = 'Key'

def get_history_data(lat, lon, start_timestamp, end_timestamp):
    url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_timestamp}&end={end_timestamp}&appid={API_key}'
    res = requests.get(url)
    return res.json()

def get_air_quality(lat, lon, start_timestamp, end_timestamp):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start_timestamp}&end={end_timestamp}&appid={API_key}'
    res = requests.get(url)
    return res.json()

bangkok_districts = {
    "Phra Nakhon": {"latitude": 13.7563, "longitude": 100.5018},
    "Dusit": {"latitude": 13.7842, "longitude": 100.5117},
    "Nong Chok": {"latitude": 13.8583, "longitude": 100.8659},
    "Bang Rak": {"latitude": 13.7259, "longitude": 100.5283},
    "Bang Khen": {"latitude": 13.8644, "longitude": 100.5843},
    "Bang Kapi": {"latitude": 13.7554, "longitude": 100.6309},
    "Pathum Wan": {"latitude": 13.7445, "longitude": 100.5342},
    "Pom Prap Sattru Phai": {"latitude": 13.7504, "longitude": 100.5097},
    "Phra Khanong": {"latitude": 13.7088, "longitude": 100.6022},
    "Min Buri": {"latitude": 13.8053, "longitude": 100.7550},
    "Lat Krabang": {"latitude": 13.7262, "longitude": 100.7562},
    "Yannawa": {"latitude": 13.6896, "longitude": 100.5369},
    "Samphanthawong": {"latitude": 13.7408, "longitude": 100.5137},
    "Phaya Thai": {"latitude": 13.7719, "longitude": 100.5385},
    "Thon Buri": {"latitude": 13.7229, "longitude": 100.4907},
    "Bangkok Yai": {"latitude": 13.7314, "longitude": 100.4806},
    "Huai Khwang": {"latitude": 13.7788, "longitude": 100.5759},
    "Khlong San": {"latitude": 13.7348, "longitude": 100.5042},
    "Taling Chan": {"latitude": 13.7702, "longitude": 100.4429},
    "Bangkok Noi": {"latitude": 13.7634, "longitude": 100.4735},
    "Bang Khun Thian": {"latitude": 13.6703, "longitude": 100.4578},
    "Phasi Charoen": {"latitude": 13.7214, "longitude": 100.4357},
    "Nong Khaem": {"latitude": 13.7153, "longitude": 100.3792},
    "Rat Burana": {"latitude": 13.6865, "longitude": 100.4925},
    "Bang Phlat": {"latitude": 13.7951, "longitude": 100.5015},
    "Din Daeng": {"latitude": 13.7663, "longitude": 100.5562},
    "Bueng Kum": {"latitude": 13.7895, "longitude": 100.6558},
    "Sathon": {"latitude": 13.7211, "longitude": 100.5289},
    "Bang Sue": {"latitude": 13.8009, "longitude": 100.5297},
    "Chatuchak": {"latitude": 13.8166, "longitude": 100.5557},
    "Prawet": {"latitude": 13.7196, "longitude": 100.6698},
    "Khlong Toei": {"latitude": 13.7126, "longitude": 100.5582},
    "Suan Luang": {"latitude": 13.7212, "longitude": 100.6406},
    "Chom Thong": {"latitude": 13.6853, "longitude": 100.4674},
    "Don Mueang": {"latitude": 13.9125, "longitude": 100.5989},
    "Ratchathewi": {"latitude": 13.7547, "longitude": 100.5342},
    "Lat Phrao": {"latitude": 13.8078, "longitude": 100.5701},
    "Watthana": {"latitude": 13.7369, "longitude": 100.5847},
    "Sai Mai": {"latitude": 13.9248, "longitude": 100.6385},
    "Khan Na Yao": {"latitude": 13.8159, "longitude": 100.6669},
    "Saphan Sung": {"latitude": 13.7610, "longitude": 100.6726},
    "Wang Thonglang": {"latitude": 13.7889, "longitude": 100.6120},
    "Khlong Sam Wa": {"latitude": 13.8647, "longitude": 100.7351},
}

# ตั้งค่าจำนวนวันที่ต้องการย้อนหลัง
days = 7
current_time = datetime.now()

# คำนวณ start และ end timestamp
end_timestamp = int(current_time.timestamp())
start_timestamp = int((current_time - timedelta(days=days)).timestamp())

# เปิดไฟล์ CSV
with open('weather_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # เขียนหัวข้อ
    writer.writerow([
        'district', 'timestamp', 'lat', 'lon', 'temp', 'feels_like', 'pressure', 'humidity',
        'clouds', 'wind_speed', 'wind_deg', 'weather_main', 'weather_desc', 'PM2_5'
    ])

    for district, coords in bangkok_districts.items():
        lat, lon = coords['latitude'], coords['longitude']

        # เรียก API
        weather_res = get_history_data(lat, lon, start_timestamp, end_timestamp)
        aqi_res = get_air_quality(lat, lon, start_timestamp, end_timestamp)

        if 'list' in weather_res and 'list' in aqi_res:
            aqi_data = {entry['dt']: entry['components']['pm2_5'] for entry in aqi_res['list']}

            for entry in weather_res['list']:
                dt = entry['dt']
                temp = entry['main']['temp']
                feels_like = entry['main']['feels_like']
                pressure = entry['main']['pressure']
                humidity = entry['main']['humidity']
                clouds = entry['clouds']['all']
                wind_speed = entry['wind']['speed']
                wind_deg = entry['wind']['deg']
                weather_main = entry['weather'][0]['main']
                weather_desc = entry['weather'][0]['description']
                pm2_5 = aqi_data.get(dt, None)  # เอาค่า PM2.5 ตาม timestamp

                writer.writerow([
                    district, dt, lat, lon, temp, feels_like, pressure, humidity,
                    clouds, wind_speed, wind_deg, weather_main, weather_desc, pm2_5
                ])
        else:
            print(f"No data for {district}")

print("Data has been written to 'weather_data.csv'")
