import pandas as pd
from helpers.settings import *
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def extract_data(train_file_path, columns, categorical_columns=CATEGORIES, interpolate=True):
    """
    Extracts data from file and create categorical columns
    :param train_file_path: string - path to file
    :param columns: List[string] - list of columns to extract from file
    :param categorical_columns: DICT[LIST[string]] - dictionary with all categorical columns and it's descriptions
    :param interpolate: boolean should interpolate NaN values and missing columns?
    :return:
    """
    # Read csv file and return
    all_data = pd.read_csv(train_file_path, usecols=columns)
    if categorical_columns is not None:
        # map categorical to columns
        for feature_name in categorical_columns.keys():
            mapping_dict = {categorical_columns[feature_name][i]: categorical_columns[feature_name][i] for i in
                            range(0, len(categorical_columns[feature_name]))}
            all_data[feature_name] = all_data[feature_name].map(mapping_dict)

        # Change mapped categorical data to 0/1 columns
        all_data = pd.get_dummies(all_data, prefix='', prefix_sep='')

    # fix missing data
    if interpolate:
        all_data = all_data.interpolate(method='linear', limit_direction='forward')

    return all_data


def preproc_data(data, norm_cols=NORM_COLS, scale_cols=SCALE_COLS, adjust_cols=ADJUST_COLUMNS):
    """
    Scales and normalize data
    :param data: pd.DataFrame
    :param norm_cols: Dict[Dict[mu: float, std: float]] - list of columns to normalize
    :param adjust_cols: Dict[Dict[amount: float]] - amount added to each col value
    :param scale_cols: Dict[Dict[min: float, max: float]] - list of columns to scale <0,1>
    :return: pd.DataFrame
    """
    # Make a copy, not to modify original data
    new_data = data.copy()
    if norm_cols:
        # Normalize
        for key, params in norm_cols.items():
            new_data[key] = (new_data[key] - params['mu'])/params['std']

    if scale_cols:
        # Scale year and week no but within (0,1)
        for key, params in scale_cols.items():
            new_data[key] = (new_data[key] + params['min'])/(params['max'] + params['min'])

    if adjust_cols:
        for key, params in adjust_cols.items():
            new_data[key] = new_data[key] + params['amount']

    return new_data
