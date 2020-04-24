import os

import pandas as pd

DATA_PATH = 'data/runs'


def load_bikes_data():
    csv_data = load_csv()
    excel_data = load_excel()
    bikes_data = pd.concat([csv_data, excel_data])

    return bikes_data


def load_csv():
    csv_files = [
            f'{DATA_PATH}/{file}' for file in os.listdir(DATA_PATH)
            if file.endswith('csv')
        ]

    data = pd.DataFrame()

    for file in csv_files:
        year_data = pd.read_csv(file)
        data = pd.concat([data, year_data]) if not data.empty else year_data

    data.drop(columns=['uid', 'Unnamed: 0'], inplace=True)

    return data


def load_excel():
    excel_files = [
        f'{DATA_PATH}/{file}' for file in os.listdir(DATA_PATH)
        if file.endswith('xlsx')
        ]

    data = pd.DataFrame()

    for file in excel_files:
        year_data = pd.read_excel(file)
        data = pd.concat([data, year_data]) if not data.empty else year_data

    data.rename({'Numer roweru': 'bike_number',
                 'Data wynajmu': 'start_time',
                 'Data zwrotu': 'end_time',
                 'Stacja wynajmu': 'rental_place',
                 'Stacja zwrotu': 'return_place'}, axis=1, inplace=True)

    data.drop(columns=['L.p.'], inplace=True)

    return data
