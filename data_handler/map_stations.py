from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from data_handler.dataset_concat import load_bikes_data


def get_stations_positions_mapping() -> Dict[str, Tuple]:
    columns = ['lat', 'lng', 'name']
    positions = pd.read_csv('data_handler/stations_positions.csv')[columns]
    new_pos = pd.read_csv(
        'data_handler/bikes_stations_2020.csv', sep=';')[columns]

    for map_ in (positions, new_pos):
        map_.drop_duplicates(subset='name', keep='first', inplace=True)
        map_.set_index('name', inplace=True)

    positions_dict = positions.to_dict(orient='index')
    positions_dict.update(new_pos.to_dict(orient='index'))

    return positions_dict


def map_stations():
    mapping = get_stations_positions_mapping()
    data = load_bikes_data()

    place_not_found = dict(lat=None, lng=None)

    lat_scaler = MinMaxScaler()
    lat_scaler.fit(
        np.array([x['lat'] for x in mapping.values()]).reshape(-1, 1)
        )

    lng_scaler = MinMaxScaler()
    lng_scaler.fit(
        np.array([x['lng'] for x in mapping.values()]).reshape(-1, 1)
        )

    for place in ('rental_place', 'return_place'):
        for coordinate, col in zip(('x', 'y'), ('lat', 'lng')):
            data[f'{place}_{coordinate}'] = data[place].apply(
                    lambda x: mapping.get(x, place_not_found)[col])
            if col == 'lat':
                data[f'{place}_{coordinate}'] = lat_scaler.transform(
                                                data[f'{place}_{coordinate}']
                                                .to_numpy()
                                                .reshape(-1, 1)
                                                )
            if col == 'lng':
                data[f'{place}_{coordinate}'] = lng_scaler.transform(
                                                data[f'{place}_{coordinate}']
                                                .to_numpy()
                                                .reshape(-1, 1)
                                                )
    data.to_csv('mapped_bikes_data.csv')


if __name__ == '__main__':
    map_stations()
