import json
import pandas as pd
from glob import glob
from datetime import datetime, timedelta
import time
from settings import *

weather_data_files = sorted(glob('./data/weather/*.json'))
# Files description https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx

COLUMNS = [
    'date',
    'time',
    'timestamp',
    'totalSnow_cm',
    'sunrise',
    'sunset',
    'tempC',
    'FeelsLikeC',
    'HeatIndexC',
    'windspeedKmph',
    'weatherCode',
    'precipMM',
    'humidity',
    'visibility',
    'pressure',
    'cloudcover'
]

concat_file = 'data/weather/weather.csv'

for file in weather_data_files:
    with open(file) as f:
        data = json.load(f)

    month_data = []
    for day in data['data']['weather']:
        for hour in day['hourly']:
            sunrise = (day['astronomy'][0]['sunrise'].split(' ')[0]).split(':')
            sunrise = int(sunrise[0]) * 60 + int(sunrise[1])
            sunset = (day['astronomy'][0]['sunset'].split(' ')[0]).split(':')
            sunset = int(sunset[0]) * 60 + int(sunset[1]) + 720
            start_time = int(hour['time'])/100*60
            datetime = datetime.strptime(day['date'], "%Y-%m-%d") + timedelta(seconds=start_time*60)
            month_data.append([
                day['date'],
                start_time,
                time.mktime(datetime.timetuple()),
                day['totalSnow_cm'],
                sunrise,
                sunset,
                hour['tempC'],
                hour['FeelsLikeC'],
                hour['HeatIndexC'],
                hour['windspeedKmph'],
                hour['weatherCode'],
                hour['precipMM'],
                hour['humidity'],
                hour['visibility'],
                hour['pressure'],
                hour['cloudcover']
            ])

    df = pd.DataFrame(month_data, columns=COLUMNS)
    path = file.split('.')[1]
    df.to_csv('.'+path+'.csv')
    df.to_csv('.'+path+'.csv')
