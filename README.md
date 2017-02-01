# Simple forecasting for timeseries

Use simple linear regression to forecast.

Usage:
```
$ pip install -r requirements.txt

# Pull last 30 days of data
$ python pull_postgresl_data.py --api_key=<datadog api key> --app_key=<datadog app key> --days-past=30 > postgres_connections.csv

# Run notebook server and open the postgresql_connections.ipynb notebook.
$ jupyter notebook
```
