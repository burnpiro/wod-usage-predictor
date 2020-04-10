import pandas as pd
import numpy as np
from glob import glob
import time
from datetime import datetime

xlsx_files = [
    'data/runs/wypozyczenia_wrm-sezon2015.xlsx',
    'data/runs/wypozyczenia_wrm-sezon2016.xlsx'
]

csv_files = glob('./data/runs/*2019*.csv')


def timeparser(start_time):
    return lambda x: time.mktime(x.timetuple()) - start_time


def strtimeparser(start_time):
    return lambda x: time.mktime(datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple()) - start_time

unique_places = []

for file in xlsx_files:
    data = pd.read_excel(file)
    year = (file.split('.')[0]).split('sezon')[-1]
    year_timestamp = time.mktime(datetime.strptime(year, "%Y").timetuple())

    print(data.head())
    print(data.columns)
    data = data.drop('L.p.', 1)
    data.columns = ['bike_number', 'start_time', 'end_time', 'rental_place', 'return_place']

    data['start_time'] = data['start_time'].apply(timeparser(year_timestamp))
    data['end_time'] = data['end_time'].apply(timeparser(year_timestamp))

    unique_places = unique_places + data['rental_place'].unique().tolist()
    unique_places = unique_places + data['return_place'].unique().tolist()

    data.to_csv('data/bike_data/' + year + '.csv', header=False)
    print((np.unique(unique_places)).size)

for file in csv_files:
    data = pd.read_csv(file)
    year = (file.split('-')[0]).split('_')[-1]
    year_timestamp = time.mktime(datetime.strptime(year, "%Y").timetuple())

    print(data.head())
    data = data.drop('uid', 1)

    data['start_time'] = data['start_time'].apply(strtimeparser(year_timestamp))
    data['end_time'] = data['end_time'].apply(strtimeparser(year_timestamp))

    unique_places = unique_places + data['rental_place'].unique().tolist()
    unique_places = unique_places + data['return_place'].unique().tolist()

    data.to_csv('data/bike_data/' + year + '.csv', mode='a', header=False)
    print((np.unique(unique_places)).size)

# uniq_data = pd.DataFrame(unique_places, columns=['place_name'])
uniq_data = pd.DataFrame(np.unique(unique_places), columns=['place_name'])

uniq_data.to_csv('data/bike_data/places.csv', header=False)
