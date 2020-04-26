import numpy as np
from sklearn.model_selection import KFold
from helpers.preprocessing_helper import *

LSTM_STEP = 1
LSTM_FUTURE_TARGET = 1
LSTM_HISTORY = 6

TRAIN_DATASET_FRAC = 0.8


def generate_lstm_data(path, cols=FULL_DATA, target_column=TARGET_COLUMN, norm_cols=NORM_COLS,
                       history_size=LSTM_HISTORY, target_size=LSTM_FUTURE_TARGET,
                       step=LSTM_STEP, train_frac=TRAIN_DATASET_FRAC, train_scale=None, index_col=DATETIME_COLUMN,
                       cat_cols=CATEGORIES,
                       scale_cols=SCALE_COLS, extra_columns=EXTRA_COLS, prepend_with_file=None):
    """
    :param path: string - path to file
    :param cols: List[string] list of all columns to be extracted from csv file
    :param target_column: string - name of the target column
    :param norm_cols: List[string] - list of columns to normalize
    :param history_size: int - how many previous records should we use for LSTM dataset
    :param target_size: int - how many outputs do we have (usually 1)
    :param step: int - if multioutput then >1 else 1
    :param train_frac: float - how to split train/val dataset
    :param train_scale: pd.DataFrame - dataset used as scale
    :param index_col: string - name of the timeseries column
    :param cat_cols: Dict[List[string]] - definition of all categorical data
    :param scale_cols: List[string] - list of columns to scale <0,1>
    :param extra_columns: List[string] - list of columns to copy without changing
    :param prepend_with_file: string - path to file used for data prepending (for testing)
    :return: Tuple(np.array, np.array, np.array, np.array, pd.DataFrame)
    """
    dataset = extract_data(path, cols, categorical_columns=cat_cols)

    if target_column not in dataset.columns:
        dataset[target_column] = pd.Series(np.zeros(len(dataset[DATETIME_COLUMN])), index=dataset.index)

    # If this is a test data then add data from previous time servies (stored in prepend_with_file)
    if prepend_with_file is not None:
        pre_dataset = extract_data(prepend_with_file, cols, categorical_columns=cat_cols)
        dataset = pre_dataset.iloc[-(history_size + 1):].append(dataset, ignore_index=True)

    # create trainscale from current dataframe
    if train_scale is None:
        train_scale = dataset.copy()

    dataset.index = dataset[index_col]
    dataset, scale = preproc_data(dataset[[DATETIME_COLUMN] + norm_cols + scale_cols + extra_columns + [TARGET_COLUMN]],
                                  norm_cols=norm_cols, scale_cols=scale_cols, train_scale=train_scale)

    # parse dataset to its values only, we don't need pandas for future processing from this point
    dataset = dataset.values
    proposed_x, proposed_y = generate_multivariate_data(dataset, target_index=-1, history_size=history_size,
                                         target_size=target_size, step=step)

    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for train_index, test_index in k_fold_data(proposed_x, proposed_y):
        x_train = proposed_x[train_index]
        y_train = proposed_y[train_index]
        x_test = proposed_x[test_index]
        y_test = proposed_y[test_index]

    return x_train, y_train, x_test, y_test, scale


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
    kfold = KFold(n_splits=folds, shuffle=True)
    return kfold.split(x, y)