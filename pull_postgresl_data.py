import argparse
import time
from datetime import datetime, timedelta

from datadog import initialize, api


def parse_date(iso_string):
    try:
        return datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key",
        help="Datadog API Key.")
    parser.add_argument("--app_key",
        help="Datadog App Key")
    parser.add_argument("--days-past", default=-1,
        help="How many days of data to fetch (measured from now).")
    parser.add_argument("--since", default=None,
                        help="Fetch data since this date (UTC).")
    parser.add_argument("--append", action='store_true',
                        help="Don't print the headers.")

    args = parser.parse_args()

    days_past = int(args.days_past)
    since = None

    if days_past > 0 and args.since:
        print "Only one of --days-past and --since allowed, not both."

    if args.since:
        since = parse_date(args.since)
        if not since:
            print "Unable to parse date: {}. Expected format: 'YYYY-MM-DDThh:mm:ss'".format(since)
            return

    if days_past < 0 and not since:
        print "One of --since and --days-past required"

    options = {
        'api_key': args.api_key,
        'app_key': args.app_key
    }

    initialize(**options)

    if not since:
        since = datetime.utcnow() - timedelta(days=days_past)

    since_epoch = int(since.strftime("%s"))
    now_epoch = int(datetime.utcnow().strftime("%s"))
    query = 'sum:postgresql.connections{environment:production,host:hqdb0}'
    seconds_per_day = 3600 * 24

    if not args.append:
        print "Datetime,Connections"

    while since_epoch < now_epoch:
        start = since_epoch
        end = since_epoch + seconds_per_day
        response = api.Metric.query(start=start, end=end, query=query)
        for point in response['series'][0]['pointlist']:
            print '{},{}'.format(datetime.fromtimestamp(int(point[0] / 1000)), point[1])

        since_epoch = end

if __name__ == "__main__":
    main()
