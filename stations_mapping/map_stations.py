import pandas as pd


def read_stations_positions():
    positions = pd.read_csv('stations_mapping\stations_positions.csv')
    return positions[['lat', 'lng', 'name']]
