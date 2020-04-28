from typing import List, Dict
import random

import folium
from folium.plugins import HeatMapWithTime


def create_heated_map(stations: Dict, with_markers=False):
    m = folium.Map(location=[51.094668940345535, 17.026888132095333],
                   tiles="Stamen Terrain",
                   zoom_start=12)

    df_hour_list = []
    for hour in range(len(stations)):
        stations_data = []
        for loc in stations[hour].values():
            stations_data.append(
                [loc['lat'], loc['lng'], loc['count']])
        df_hour_list.append(stations_data)

    HeatMapWithTime(df_hour_list,
                    radius=8,
                    gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange',
                              1: 'red'},
                    min_opacity=0.8,
                    max_opacity=1,
                    use_local_extrema=True).add_to(m)

    if with_markers:
        for station, loc in stations[0].items():
            folium.Marker(
                [loc['lat'], loc['lng']],
                popup=f'<i>{station}</i>'
            ).add_to(m)

    m.save('bikes_usage_map.html')


def create_station_map(stations_d: Dict):
    m = folium.Map(location=[51.094668940345535, 17.026888132095333],
                   tiles="Stamen Terrain",
                   zoom_start=12)

    tooltip = 'Click me!'

    for station, loc in stations_d.items():
        folium.Marker(
            [loc['lat'], loc['lng']],
            popup=f'<i>{station}</i>',
            tooltip=tooltip
        ).add_to(m)

    m.save('station_map.html')
