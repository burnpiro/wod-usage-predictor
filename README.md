# Wrocław Open Dataset - WRM usage predictor

ML project to predict usage of WRM

## Getting Started

### Prerequisites

Packages:
```
tensorflow>=2.1
scikit-learn
seaborn>=0.10.0
pandas>=1.0.1
notebook>=6.0.3
matplotlib>=3.2.0
jupyter-core>=4.6.3
```

### Installing

Best way to install dependencies and avoid unnecessary problems is to setup [Anaconda](https://www.anaconda.com/) env and run following command inside the environment

```
pip install -r requirements.txt
```

after that you should be able to run:

```
jupyter notebook
```

to open one of the notebooks.

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Data Processing

- [Weather Data Source](http://worldweatheronline.com)
- [Usage Source](https://www.wroclaw.pl/open-data/dataset/przejazdy-wroclawskiego-roweru-miejskiego-archiwalne)

For weather data description check Files description [This Link](https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx)

For each day we're extracting data in format:
```
[
    'date',
    'time',
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
```

Most of the data comes directly from the source except:
- **time** - source data converted from string `1300` to number `13*60`
- **sunrise** - date converted from `HH:mm AM` to minutes, started from midnight
- **sunset** - date converted from `HH:mm PM` to minutes, started from midnight

#### To run data processing:
```bash
python weather_parser.py
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Tensorflow](https://www.tensorflow.org/) - An end-to-end open source machine learning platform for everyone
* [Pandas](https://pandas.pydata.org/) - Open source data analysis and manipulation tool
* [WOD](https://www.wroclaw.pl/open-data/) - Wroclaw Open Dataset

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [https://github.com/burnpiro/wod-usage-predictor/tags](https://github.com/burnpiro/wod-usage-predictor/tags). 

## Authors

See also the list of [contributors](https://github.com/burnpiro/wod-usage-predictor/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
