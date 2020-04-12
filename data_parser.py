import pandas as pd
import numpy as np
import os
from glob import glob
import time
from datetime import datetime
from settings import COLUMNS

data_path = 'data/bike_data/'

xlsx_files = [
    'data/runs/wypozyczenia_wrm-sezon2015.xlsx',
    'data/runs/wypozyczenia_wrm-sezon2016.xlsx'
]

csv_files = sorted(glob('./data/runs/*2019*.csv'))

existing_files = sorted(glob(data_path + '*_temp.csv'))

# Remove existing temp files
for file in existing_files:
    os.remove(file)

unique_places = []

weather_data = pd.read_csv('data/weather/weather.csv', names=COLUMNS)
weather_data['timestamp'] = weather_data['timestamp'].astype(float)


def timeparser(start_time):
    return lambda x: time.mktime(x.timetuple()) - start_time


def strtimeparser(start_time):
    return lambda x: time.mktime(datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple()) - start_time


def trim_and_remove_slash(s):
    return s.strip().replace('/', '-').replace('"', '').replace(',', ' -')


def parse_x(x, weather_column):
    year_time = time.mktime(datetime.strptime(x['year'], "%Y").timetuple())
    column_data = weather_data[(weather_data['timestamp'] < year_time + x['start_time']) & (
            weather_data['timestamp'] >= year_time + x['start_time'] - (60 * 60))][
        weather_column]
    if len(column_data.values) == 0:
        # IF THERE IS NOT column_data that means there is a timezone change and we're missing an hour
        # Solution is to get closes previous weather data and use it instead
        column_data = weather_data[(weather_data['timestamp'] < year_time + x['start_time'])][
            weather_column].tail(1)
    return column_data.values[0]


def extract_weather_column(weather_column):
    return lambda x: parse_x(x, weather_column)


for file in xlsx_files:
    print('Reading: ' + file)
    data = pd.read_excel(file)
    print('Loaded: ' + file)
    year = (file.split('.')[0]).split('sezon')[-1]
    year_timestamp = time.mktime(datetime.strptime(year, "%Y").timetuple())

    data = data.drop('L.p.', 1)
    data.columns = ['bike_number', 'start_time', 'end_time', 'rental_place', 'return_place']
    data = data[['bike_number', 'start_time', 'end_time', 'rental_place', 'return_place']]

    data['year'] = year
    data['week_day'] = data['start_time'].apply(lambda x: x.weekday())
    data['start_time'] = data['start_time'].apply(timeparser(year_timestamp)).astype(int)
    data['end_time'] = data['end_time'].apply(timeparser(year_timestamp)).astype(int)
    data['rental_place'] = data['rental_place'].apply(trim_and_remove_slash)
    data['return_place'] = data['return_place'].apply(trim_and_remove_slash)

    print('Copying data from weather data into rows: ' + file)
    for column in COLUMNS[3:]:
        print('Processing: ' + column)
        data[column] = data[['start_time', 'year']].apply(extract_weather_column(column), axis=1)

    unique_places = unique_places + data['rental_place'].unique().tolist()
    unique_places = unique_places + data['return_place'].unique().tolist()

    print('Preview')
    print(data.head())
    print('Updating output file')
    data.to_csv(data_path + year + '_temp.csv', header=False, index=False)
    print((np.unique(unique_places)).size)

for file in csv_files:
    print('Reading: ' + file)
    data = pd.read_csv(file)
    print('Loaded: ' + file)
    year = (file.split('-')[0]).split('_')[-1]
    year_timestamp = time.mktime(datetime.strptime(year, "%Y").timetuple())

    data = data[['bike_number', 'start_time', 'end_time', 'rental_place', 'return_place']]

    data['year'] = year
    data['week_day'] = data['start_time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday())
    data['start_time'] = data['start_time'].apply(strtimeparser(year_timestamp)).astype(int)
    data['end_time'] = data['end_time'].apply(strtimeparser(year_timestamp)).astype(int)
    data['rental_place'] = data['rental_place'].apply(trim_and_remove_slash)
    data['return_place'] = data['return_place'].apply(trim_and_remove_slash)

    print('Copying data from weather data into rows: ' + file)
    for column in COLUMNS[3:]:
        print('Processing: ' + column)
        data[column] = data[['start_time', 'year']].apply(extract_weather_column(column), axis=1)

    unique_places = unique_places + data['rental_place'].unique().tolist()
    unique_places = unique_places + data['return_place'].unique().tolist()

    print('Preview')
    print(data.head())
    print('Updating output file')
    data.to_csv(data_path + year + '_temp.csv', mode='a', header=False, index=False)
    print((np.unique(unique_places)).size)

uniq_data = pd.DataFrame(np.unique(unique_places), columns=['place_name'])

uniq_data.to_csv(data_path + 'places.csv', header=False)
