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

new_model = tf.keras.models.load_model('model/saved_model/model-20200429-114857.h5')

dataset_file = 'data/test_data.csv'
stations_file = './data/stations.csv'
stations = pd.read_csv(stations_file, usecols=STATIONS_COLUMNS, sep=';')

x, y = generate_lstm_data(
    dataset_file,
    history_size=HISTORY_SIZE,
    index_col='timestamp',
    norm_cols=NORM_COLS,
    scale_cols=SCALE_COLS,
    adjust_cols=ADJUST_COLUMNS,
    cat_cols=None,
    extra_columns=EXTRA_COLS
)

val_data_single = tf.data.Dataset.from_tensor_slices((x, y))
val_data_single = val_data_single.batch(len(y))
new_prediction = None
for x, y in val_data_single.take(1):
    new_predictions = new_model.predict(x)

ADJUST_COLUMNS = {
    'lat': {
        'amount': -51.0
    },
    'lng': {
        'amount': -16.0
    }
}


def parse_x(x):
    x = x.numpy()
    x[1] = x[1] - ADJUST_COLUMNS['lat']['amount']
    x[2] = x[2] - ADJUST_COLUMNS['lng']['amount']
    x[3] = x[3] * 1380
    return [x[3], x[1], x[2]]

pred = []
for i, val in enumerate(new_predictions):
    pred.append(parse_x(x) + y[i])
    # Display progess bar
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%% (%d/%d)" % (
        '=' * int(20 * (i + 1) / len(y)), int(100 * (i + 1) / len(y)), (i + 1),
        len(y)))
    sys.stdout.flush()


exit_file = pd.DataFrame(pred, columns=['time', 'lat', 'lng', 'count'])
exit_file.to_csv('pred.csv')