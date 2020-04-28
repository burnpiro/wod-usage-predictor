from data_handler.map_stations import get_stations_positions_mapping
from results_visualizations.create_map import create_station_map, create_heated_map

if __name__ == '__main__':
    stations = get_stations_positions_mapping()
    create_station_map(stations)

    """
        heated map needs input in form of list of
        Dict station_name: {lat: val, lng: val, rents: val}
        for each hour
    """
    create_heated_map(stations, with_markers=False)
