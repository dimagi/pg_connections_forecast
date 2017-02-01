import argparse
import time
from datetime import datetime

from datadog import initialize, api


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("api_key",
        help="Datadog API Key.")
    parser.add_argument("app_key",
        help="Datadog App Key")
    parser.add_argument("--days-past", default=30,
        help="How many days of data to fetch")

    args = parser.parse_args()

    days_past = int(args.days_past)

    options = {
        'api_key': args.api_key,
        'app_key': args.app_key
    }

    initialize(**options)

    now = int(time.time())
    query = 'sum:postgresql.connections{environment:production,host:hqdb0}'
    seconds_per_day = 3600 * 24

    print "Datetime,Connections"
    for day in range(-days_past, 0):
        start = now + (day * seconds_per_day)
        end = now + ((day + 1) * seconds_per_day)
        response = api.Metric.query(start=start, end=end, query=query)
        for point in response['series'][0]['pointlist']:
            print '{},{}'.format(datetime.utcfromtimestamp(int(point[0]/1000)), point[1])

if __name__ == "__main__":
    main()
