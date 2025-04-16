import threading

import requests
import time
from lib import calculate_heat_index, display_data, evaluate_advance_conditions

city = "Georgetown"
api_key = "9f585271cac728f87204cbab41116f1b"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

data={}
aqi_data={}

def fetchdata():
    global data, aqi_data
    response = requests.get(url)
    data = response.json()

    aqi_request_url = 'https://api.waqi.info/feed/@9489/?token=8073382e8b7155e691f68762e30b59a4c517d9e3'

    aqi_res = requests.get(aqi_request_url)
    aqi_data = aqi_res.json()

    print('fetched data')

    return {'data': data, 'aqi_data': aqi_data}

def fetchdataloop():
    while True:
        global data, aqi_data
        response = requests.get(url)
        data = response.json()

        aqi_request_url = 'https://api.waqi.info/feed/@9489/?token=8073382e8b7155e691f68762e30b59a4c517d9e3'

        aqi_res = requests.get(aqi_request_url)
        aqi_data = aqi_res.json()

        print('fetched data')

        time.sleep(30)


data_thread = threading.Thread(
    target=fetchdataloop, daemon=True
)
data_thread.start()

fetchdata()

temperature = data['main']['temp']
humidity = data['main']['humidity']
pressure = data['main']['pressure']
uv_intensity = 1
light_intensity=1
elevation = 117
latitude=data['coord']['lat']
longitude=data['coord']['lon']
air_quality=aqi_data['data']['aqi']
wind_speed=data['wind']['speed']
wind_direction=data['wind']['deg']
sunrise_raw=data['sys']['sunrise']
sunset_raw=data['sys']['sunset']
sunrise=time.strftime('%I:%M %p', time.localtime(sunrise_raw))
sunset=time.strftime('%I:%M %p', time.localtime(sunset_raw))
clouds=data['clouds']['all']
heat_index=calculate_heat_index(temperature, humidity)
current_time = time.localtime()
rating, message = evaluate_advance_conditions(current_time, temperature, humidity, uv_intensity, light_intensity, pressure, elevation, heat_index, air_quality, wind_speed, wind_direction, clouds)

while True:
    current_time=time.localtime()
    current_date=time.strftime('%Y-%m-%d', current_time)
    current_time=time.strftime('%H:%M:%S', current_time)
    display_data(True, current_date, current_time, temperature, humidity, heat_index, light_intensity, uv_intensity, pressure, elevation, latitude, longitude, rating, message, air_quality, wind_speed, wind_direction, sunrise, sunset, clouds)
    time.sleep(1)
