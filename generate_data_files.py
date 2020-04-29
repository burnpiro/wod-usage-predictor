import tensorflow as tf
from model.create_model import get_model
from datetime import datetime
import pandas as pd
import numpy as np
import sys
import pickle
import math

from model.data_preprocessor import generate_lstm_data
from helpers.settings import *
from model.config import HISTORY_SIZE, ROW_LENGTH

EVALUATION_INTERVAL = 200
EPOCHS = 2
BATCH_SIZE = 8
BUFFER_SIZE = 500
dataset_file = './data/model_input2.csv'
stations_file = './data/stations.csv'
NUM_OF_HOURS_PER_FILE = 1000

if __name__ == '__main__':

    stations = pd.read_csv(stations_file, usecols=STATIONS_COLUMNS, sep=';')
    num_of_hours = 0
    temp_dataset_x = np.array(())
    temp_dataset_y = np.array(())
    num_of_stations = len(stations)
    num_of_active_stat = 0
    for s_id, station in stations.iterrows():
        x, y = generate_lstm_data(
            dataset_file,
            history_size=HISTORY_SIZE,
            index_col='timestamp',
            norm_cols=NORM_COLS,
            scale_cols=SCALE_COLS,
            adjust_cols=ADJUST_COLUMNS,
            filter_cols={
                'lat': [
                    station['lat']
                ],
                'lng': [
                    station['lng']
                ]
            },
            cat_cols=None,
            extra_columns=EXTRA_COLS
        )
        if np.sum(y) == 0:
            continue
        num_of_active_stat += 1
        temp_dataset_x = np.append(temp_dataset_x, x)
        temp_dataset_y = np.append(temp_dataset_y, y)
        print(np.sum(y))
        print(np.sum(temp_dataset_y))
        for i in range(len(temp_dataset_y)):
            if temp_dataset_y[i] > 0:
                print(temp_dataset_y[i])
        # every sample has the same size, only thing we need to know is how big is it
        num_of_hours = x.shape[0]
        # Display progess bar
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% (%d/%d)" % (
            '=' * int(20 * (s_id + 1) / num_of_stations), int(100 * (s_id + 1) / num_of_stations), (s_id + 1),
            num_of_stations))
        sys.stdout.flush()

    temp_dataset_x = temp_dataset_x.reshape((-1, HISTORY_SIZE, ROW_LENGTH))
    print(temp_dataset_x.shape)
    print(temp_dataset_y.shape)
    print(np.sum(temp_dataset_y))
    dataset_x = []
    dataset_y = []
    max_i = 0
    for i in range(num_of_hours):
        for s_id in range(num_of_active_stat):
            dataset_x.append(temp_dataset_x[i + s_id])
            dataset_y.append(temp_dataset_y[i + s_id])
        print(np.sum(dataset_y), 'dataset y')
        print(np.sum(temp_dataset_y), 'temp dataset y')

        # Display progess bar
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% (%d/%d)" % (
            '=' * int(20 * (i + 1) / num_of_hours), int(100 * (i + 1) / num_of_hours), i + 1, num_of_hours))
        sys.stdout.flush()

        max_i = i
        if i % NUM_OF_HOURS_PER_FILE == 0 and i != 0:
            print(np.sum(dataset_y), 'dataset y')
            with open(f'model/train_data/train_x_{str(math.ceil(i / NUM_OF_HOURS_PER_FILE))}.pkl', 'wb') as filehandler:
                # store the data as binary data stream
                pickle.dump(dataset_x, filehandler)
                dataset_x = []

            with open(f'model/train_data/train_y_{str(math.ceil(i / NUM_OF_HOURS_PER_FILE))}.pkl', 'wb') as filehandler:
                # store the data as binary data stream
                pickle.dump(dataset_y, filehandler)
                dataset_y = []

    # if there is anything left save it as a last file
    if len(dataset_x) > 0:
        with open(f'model/train_data/train_x_{str(math.ceil(max_i / NUM_OF_HOURS_PER_FILE))}.pkl', 'wb') as filehandler:
            # store the data as binary data stream
            pickle.dump(dataset_x, filehandler)
            dataset_x = []

        with open(f'model/train_data/train_y_{str(math.ceil(max_i / NUM_OF_HOURS_PER_FILE))}.pkl', 'wb') as filehandler:
            # store the data as binary data stream
            pickle.dump(dataset_y, filehandler)
            dataset_y = []

    print('done')
