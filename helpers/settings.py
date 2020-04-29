WEATHER_CODES = {
    113: 'Sunny',
    116: 'Partly cloudy',
    119: 'Cloudy',
    122: 'Overcast',
    143: 'Mist',
    176: 'Patchy rain possible',
    179: 'Patchy snow possible',
    182: 'Patchy sleet possible',
    185: 'Patchy freezing drizzle possible',
    200: 'Thundery outbreaks possible',
    227: 'Blowing snow',
    230: 'Blizzard',
    248: 'Fog',
    260: 'Freezing fog',
    263: 'Patchy light drizzle',
    266: 'Light drizzle',
    281: 'Freezing drizzle',
    284: 'Heavy freezing drizzle',
    293: 'Patchy light rain',
    296: 'Light rain',
    299: 'Moderate rain at times',
    302: 'Moderate rain',
    305: 'Heavy rain at times',
    308: 'Heavy rain',
    311: 'Light freezing rain',
    314: 'Moderate or Heavy freezing rain',
    317: 'Light sleet',
    320: 'Moderate or heavy sleet',
    323: 'Patchy light snow',
    326: 'Light snow',
    329: 'Patchy moderate snow',
    332: 'Moderate snow',
    335: 'Patchy heavy snow',
    338: 'Heavy snow',
    350: 'Ice pellets',
    353: 'Light rain shower',
    356: 'Moderate or heavy rain shower',
    359: 'Torrential rain shower',
    362: 'Light sleet showers',
    365: 'Moderate or heavy sleet showers',
    368: 'Light snow showers',
    371: 'Moderate or heavy snow showers',
    374: 'Light showers of ice pellets',
    377: 'Moderate or heavy showers of ice pellets',
    386: 'Patchy light rain in area with thunder',
    389: 'Moderate or heavy rain in area with thunder',
    392: 'Patchy light snow in area with thunder',
    395: 'Moderate or heavy snow in area with thunder'
}

INPUT_FILE_COLUMNS = [
    'name', 'lat', 'lng', 'timestamp', 'year', 'week_day', 'time', 'totalSnow_cm', 'sunrise', 'sunset', 'tempC',
    'FeelsLikeC', 'HeatIndexC', 'windspeedKmph', 'weatherCode', 'precipMM', 'humidity', 'visibility', 'pressure',
    'cloudcover', 'num_of_rents'
]

WEATHER_DATA_COLUMNS = [
    'date',
    'time',
    'timestamp',
    'totalSnow_cm',
    'sunrise',
    'sunset',
    'tempC',
    'FeelsLikeC',
    'HeatIndexC',
    'windspeedKmph',
    'weatherCode',
    'precipMM',
    'humidity',
    'visibility',
    'pressure',
    'cloudcover'
]

STATIONS_COLUMNS = [
    'station_nbr',
    'name',
    'lat',
    'lng',
]

# Target for given station
TARGET_COLUMN = 'num_of_rents'

# TODO Update columns when bikedata is processed into station coordinates
BIKE_COLUMNS = [
    'bike_number',
    'start_time',
    'end_time',
    'rental_place',
    'return_place',
    'year',
    'week_day',
]

WEATHER_COLS = [
    'totalSnow_cm',
    'sunrise',
    'sunset',
    'tempC',
    'FeelsLikeC',
    'HeatIndexC',
    'windspeedKmph',
    'weatherCode',
    'precipMM',
    'humidity',
    'visibility',
    'pressure',
    'cloudcover'
]

GROUP_COLS = [
    'year',
    'time',
    'timestamp'
]

# List of categorical columns
CATEGORIES = {
    'weatherCode': WEATHER_CODES
}

# Columns to be normalized
# TODO Update columns when bikedata is processed into station coordinates
NORM_COLS = {
    'tempC': {
        'mu': 8,
        'std': 3
    },
    'FeelsLikeC': {
        'mu': 8,
        'std': 3
    },
    'HeatIndexC': {
        'mu': 8,
        'std': 3
    },
    'pressure': {
        'mu': 1013,
        'std': 15
    },
}

ADJUST_COLUMNS = {
    'lat': {
        'amount': -51.0
    },
    'lng': {
        'amount': -16.0
    }
}

# Columns to be scaled from 0-1
# TODO Update columns when bikedata is processed into station coordinates
SCALE_COLS = {
    'time': {
        'min': 0,
        'max': 1380
    },
    'sunrise': {
        'min': 0,
        'max': 1380
    },
    'sunset': {
        'min': 0,
        'max': 1380
    },
    'windspeedKmph': {
        'min': 0,
        'max': 150
    },
    'humidity': {
        'min': 0,
        'max': 100
    },
    'visibility': {
        'min': 0,
        'max': 100
    },
    'cloudcover': {
        'min': 0,
        'max': 100
    },
}

# Columns which are copied from dataset directly
EXTRA_COLS = [
    'week_day',
    'totalSnow_cm',
    'precipMM'
]

DATETIME_COLUMN = 'start_time'

FULL_DATA = BIKE_COLUMNS + WEATHER_COLS + [TARGET_COLUMN]
