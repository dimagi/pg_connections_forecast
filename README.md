# Simple forecasting for timeseries

Use simple linear regression to forecast.

Usage:
```
$ pip install -r requirements.txt

# Pull last 30 days of data
$ python pull_postgresl_data.py --api_key=<datadog api key> --app_key=<datadog app key> --days-past=30 > postgres_connections.csv

# Pull all data since last pull and append it to the current data file
$ tail -n 1 postgres_connections.csv
2017-03-20 09:30:00,53.1428563595

$ python pull_postgresl_data.py --api_key=<datadog api key> --app_key=<datadog app key> --since=2017-03-20T09:30:00 --append >> postgres_connections.csv

# Run notebook server and open the postgresql_connections.ipynb notebook.
$ jupyter notebook
```
