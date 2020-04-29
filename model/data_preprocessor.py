import numpy as np
from sklearn.model_selection import KFold, TimeSeriesSplit
from helpers.settings import *
from model.preprocessing_helper import *
from model.config import HISTORY_SIZE
from datetime import datetime

LSTM_STEP = 1
LSTM_FUTURE_TARGET = 1
LSTM_HISTORY = HISTORY_SIZE

TRAIN_DATASET_FRAC = 0.8


def generate_lstm_data(path, cols=INPUT_FILE_COLUMNS, target_column=TARGET_COLUMN, norm_cols=NORM_COLS,
                       history_size=LSTM_HISTORY, target_size=LSTM_FUTURE_TARGET,
                       step=LSTM_STEP, index_col=DATETIME_COLUMN,
                       filter_cols=None,
                       cat_cols=CATEGORIES, adjust_cols=ADJUST_COLUMNS,
                       scale_cols=SCALE_COLS, extra_columns=EXTRA_COLS):
    """
    :param path: string - path to file
    :param cols: List[string] list of all columns to be extracted from csv file
    :param target_column: string - name of the target column
    :param norm_cols: Dict[Dict[mu: float, std: float]] - list of columns to normalize
    :param history_size: int - how many previous records should we use for LSTM dataset
    :param target_size: int - how many outputs do we have (usually 1)
    :param step: int - if multioutput then >1 else 1
    :param index_col: string - name of the timeseries column
    :param filter_cols: Dict[List[any]] - filters colums from Dict keys by list of values from the List
    :param cat_cols: Dict[List[string]] - definition of all categorical data
    :param adjust_cols: Dict[Dict[amount: float]] - amount added to each col value
    :param scale_cols: Dict[Dict[min: float, max: float]] - list of columns to scale <0,1>
    :param extra_columns: List[string] - list of columns to copy without changing
    :return: Tuple(np.array, np.array)
    """
    dataset = pd.read_csv(path, usecols=cols)

    if target_column not in dataset.columns:
        dataset[target_column] = pd.Series(np.zeros(len(dataset[index_col])), index=dataset.index)

    dataset.index = dataset[index_col]

    # test_y = dataset[dataset[target_column] > 0]
    # print(test_y.describe())
    # print(dataset.describe())

    if filter_cols is not None:
        for key, value in filter_cols.items():
            dataset = dataset[dataset[key].isin(value)]

    dataset['day_of_year'] = dataset[index_col].apply(lambda x: datetime.fromtimestamp(x).timetuple().tm_yday / 365)

    cols_to_extract = ['day_of_year'] + list(adjust_cols.keys()) + list(
        scale_cols.keys()) + list(norm_cols.keys()) + extra_columns + [target_column]
    # print(cols_to_extract)
    # print(dataset.columns)
    # print(dataset[target_column].describe(), filter_cols)
    dataset = preproc_data(
        dataset[cols_to_extract],
        norm_cols=norm_cols,
        scale_cols=scale_cols,
        adjust_cols=adjust_cols
    )

    # parse dataset to its values only, we don't need pandas for future processing from this point
    dataset = dataset.values
    # print(dataset[:5])
    proposed_x, proposed_y = generate_multivariate_data(dataset, target_index=-1, history_size=history_size,
                                                        target_size=target_size, step=step)

    # print(np.sum(proposed_y))
    return proposed_x, proposed_y


def generate_multivariate_data(dataset, history_size=LSTM_HISTORY, target_size=LSTM_FUTURE_TARGET,
                               step=LSTM_STEP, target_index=-1, target=None):
    """

    :param dataset: np.array
    :param history_size: int - how many previous records should we use for LSTM dataset
    :param target_size: int - how many outputs do we have (usually 1)
    :param step: int - if multioutput then >1 else 1
    :param target_index: int - index of the target column
    :param target: np.array - should be set if dataset doesn't contain target
    :return: Tuple(np.array, np.array)
    """

    # if there is no explicit target when get target from dataset
    if target is None:
        target = dataset[:, target_index]
        dataset = dataset[:, :target_index]

    dataset_size = len(dataset)
    train_to_idx = dataset_size - target_size
    start_train_idx = history_size

    data = []
    labels = []
    for i in range(start_train_idx, train_to_idx):
        indices = range(i - history_size, i, step)
        data.append(dataset[indices])

        labels.append(target[i + target_size])

    return np.array(data), np.array(labels)


def k_fold_data(x, y, folds=10):
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    kfold = KFold(n_splits=folds, shuffle=True)
    for train_index, test_index in kfold.split(x, y):
        x_train = x[train_index]
        y_train = y[train_index]
        x_test = x[test_index]
        y_test = y[test_index]
    return x_train, y_train, x_test, y_test


def k_fold_ts_data(x, y, folds=10):
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    kfold = TimeSeriesSplit(n_splits=folds)
    for train_index, test_index in kfold.split(x, y):
        x_train = x[train_index]
        y_train = y[train_index]
        x_test = x[test_index]
        y_test = y[test_index]
    return x_train, y_train, x_test, y_test
