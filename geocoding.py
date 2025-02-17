import requests
import pandas as pd

# Step 1: API Geo untuk mendapatkan latitude dan longitude Surabaya
geo_url = "http://api.openweathermap.org/geo/1.0/direct"
geo_params = {
    'q': 'Surabaya,ID',  # Kota dan negara
    'limit': 1,          # Batas hasil
    'appid': '633d312144412b2b11cbe794717b314f'  # API key
}

geo_response = requests.get(geo_url, params=geo_params)

# Mengecek apakah request berhasil
if geo_response.status_code == 200:
    geo_data = geo_response.json()
    
    # Memastikan data lokasi ditemukan
    if geo_data:
        # Ambil latitude dan longitude dari hasil
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        print(f"Latitude: {lat}, Longitude: {lon}")
        
        # Rentang waktu (dalam format UNIX timestamp)
        start_time = 1704067200  # Contoh: 1 Januari 2024 00:00:00 UTC
        end_time = 1735689599    # Contoh: 1 Januari 2024 23:59:59 UTC
        
        # Step 2: API untuk air pollution forecast menggunakan lat dan lon
        air_pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution/history"
        air_pollution_params = {
            'lat': lat,            # Latitude dari Geo API
            'lon': lon,            # Longitude dari Geo API
            'start': start_time,   # Waktu mulai
            'end': end_time,       # Waktu akhir
            'appid': '3d43be630394bd2f9216b92e98e73afe'  # API key
        }
        
        # Memanggil API Air Pollution Forecast
        air_pollution_response = requests.get(air_pollution_url, params=air_pollution_params)
        
        # Mengecek apakah request berhasil
        if air_pollution_response.status_code == 200:
            air_pollution_data = air_pollution_response.json()
            
            # Memastikan data ada sebelum proses lebih lanjut
            if 'list' in air_pollution_data and air_pollution_data['list']:
                # Menyimpan data ke dalam CSV
                df = pd.json_normalize(air_pollution_data['list'])  # Memindahkan data JSON ke DataFrame
                df.to_csv('airpollution_surabaya2024.csv', index=False)      # Menyimpan ke CSV
                print("Data berhasil disimpan ke 'airpollution_surabaya2024.csv'")
            else:
                print("Tidak ada data polusi udara yang tersedia dalam rentang waktu tersebut.")
        else:
            print(f"Error Air Pollution API: {air_pollution_response.status_code}")
    else:
        print("Data lokasi tidak ditemukan.")
else:
    print(f"Error Geo API: {geo_response.status_code}")
