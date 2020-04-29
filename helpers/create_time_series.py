import os
import sys
from helpers.preprocessing_helper import *
import time
from datetime import datetime


# run weather_parser.py to generate data/weather.csv before

def sum_times(x, year, time_col):
    year_time = time.mktime(datetime.strptime(str(x[year]), "%Y").timetuple())

    return year_time + int(x[time_col])


def time_concat(time_col):
    return lambda x: sum_times(x, 'year', time_col)


def generate_weather_time_series(out_file='data/model_input2.csv',
                                 weather_file='data/weather/weather.csv',
                                 stations_file='data/stations.csv',
                                 bike_files=[
                                     {
                                         'file': 'data/bike_data/2015_temp.csv',
                                         'year_col': 'year',
                                     },
                                     {
                                         'file': 'data/bike_data/2016_temp.csv',
                                         'year_col': 'year',
                                     },
                                     {
                                         'file': 'data/bike_data/2019_temp.csv',
                                         'year_col': 'year',
                                     },
                                 ],
                                 weather_cols=WEATHER_DATA_COLUMNS,
                                 stations_cols=STATIONS_COLUMNS,
                                 bike_cols=BIKE_COLUMNS + WEATHER_COLS,
                                 weather_time_column='timestamp',
                                 bike_time_column='start_time',
                                 station_map_cols=['name'],
                                 bike_map_cols=['rental_place'],
                                 cols_from_weather=['timestamp', 'year', 'week_day', 'time'] + WEATHER_COLS,
                                 cols_from_station=['name', 'lat', 'lng'],
                                 target_col_name=TARGET_COLUMN,
                                 ):
    """
    :param out_file: string - path for output csv file
    :param weather_file: string - path to csv file with weather data to process
    :param stations_file: string - path to csv file with stations data to process
    :param bike_files: List[Dict[file: string, year: int]] - list of files to process with year description
    :param weather_cols: List[string] - list of columns in weather file
    :param stations_cols: List[string] - list of columns in stations file
    :param bike_cols: List[string] - list of columns in bike files
    :param weather_time_column: name of weather column to use as time
    :param bike_time_column: name of bike column to use as time
    :param station_map_cols: string - name of column with timestamp data to use for mapping
    :param bike_map_cols: string - name of column with timestamp data to use for mapping (+ year timestamp)
    :param cols_from_weather: List[string] - list of columns to extract from weather file into out file
    :param cols_from_station: List[string] - list of columns to extract from stations file into out file
    :param target_col_name: string - what should be the name of bike count per row
    :return: None
    """

    if not os.path.isfile(weather_file):
        raise ValueError(f'There is no file in {weather_file}')

    if not os.path.isfile(stations_file):
        raise ValueError(f'There is no file in {stations_file}')

    weather = pd.read_csv(weather_file, header=None, names=weather_cols)
    weather['year'] = weather[weather_time_column].apply(lambda x: datetime.fromtimestamp(x).year)
    weather['week_day'] = weather[weather_time_column].apply(lambda x: datetime.fromtimestamp(x).weekday())
    stations = pd.read_csv(stations_file, usecols=stations_cols, sep=';')
    data = None

    for bike_data in bike_files:
        print('Reading: ' + bike_data['file'])

        data_to_append = pd.read_csv(bike_data['file'], header=None, names=bike_cols)
        data_to_append['year'] = data_to_append[bike_data['year_col']]
        data_to_append['full_timestamp'] = data_to_append[[bike_time_column, 'year']].apply(
            time_concat(bike_time_column), axis=1).astype(int)

        if data is None:
            data = data_to_append
        else:
            data.append(data_to_append, ignore_index=True)
        print('Appended: ' + bike_data['file'])

    print('All bike files read')

    num_of_weather_inputs = len(weather.index)
    print('Generating timeseries data')

    # print(data.head(50))
    out_cols = cols_from_station + cols_from_weather + [target_col_name]
    out_dataset = []

    for w_id, hour_weather in weather.iterrows():
        # get all bike data which are in weather time period
        transactions_matching_conditions = data[
            (data['full_timestamp'] >= hour_weather[weather_time_column]) &
            (data['full_timestamp'] < hour_weather[weather_time_column] + (60 * 60))
            ]

        for s_id, station in stations.iterrows():
            transactions_per_station = transactions_matching_conditions

            # I know that looks bad but we cannot apply logic conditions on multiple columns without crushing pandas like:
            # MemoryError: Unable to allocate 5.18 TiB for an array with shape (843951, 843951) and data type float64
            for id, col in enumerate(station_map_cols):
                transactions_per_station = transactions_per_station[
                    transactions_per_station[bike_map_cols[id]] == station[station_map_cols[id]]
                    ]

            # Create row with data for one hour per station
            row_data = station[cols_from_station].tolist() + hour_weather[cols_from_weather].tolist() + [
                transactions_per_station.shape[0]]

            # Add current row to dataset
            out_dataset.append(row_data)

        # Display progess bar
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% (%d/%d)" % (
            '=' * int(20 * w_id / num_of_weather_inputs), int(100 * w_id / num_of_weather_inputs), w_id,
            num_of_weather_inputs))
        sys.stdout.flush()

    out_dataset = pd.DataFrame(out_dataset, columns=out_cols)
    out_dataset.to_csv(out_file, header=True, index=False)
