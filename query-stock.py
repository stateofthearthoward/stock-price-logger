import argparse
from datetime import datetime, timezone
import json
import requests
import logging
import os.path
from pathlib import Path

def get_data(symbol) -> dict:
    # This is the URL that is called on the page https://www.cnbc.com/quotes/.SPX
    # https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=.SPX&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1

    try:
        p = {'symbols': symbol, 'requestMethod':'itv', 'noform':1, 'partnerId':2,'fund':1, 'exthrs':1, 'output':'json', 'events':1}
        r = requests.get('https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol', params=p)
        r.raise_for_status()
        data = r.json()
    except requests.ConnectionError as e:
        # to test this, use bad host name like cnbc404.com
        print("Connection error: ", e)
        raise SystemExit from e
    except requests.exceptions.HTTPError as e:
        # to test this, use "quote404-html-webservice" in url
        print("Failed to make url request: ", e)
        raise SystemExit from e
    except requests.exceptions.JSONDecodeError as e:
        # to test this, use output type xml in the params
        print("Failed to decode the json response: ", e)
        print("data: ", r.text)
        raise SystemExit from e

    #sanity check the API returned data and prune each layer
    if (not isinstance(data, dict) or "FormattedQuoteResult" not in data):
        print("data format error, expected dict: ", data)
        raise SystemExit
    data = data["FormattedQuoteResult"]

    if (not isinstance(data, dict) or "FormattedQuote" not in data):
        print("data format error, expected dict: ", data)
        raise SystemExit
    data = data["FormattedQuote"]

    # we are only requesting a single symbol to be returned so the list has a single entry
    if (not isinstance(data, list) or len(data) != 1):
        print("data format error, expected list: ", data)
        raise SystemExit
    data = data[0]

    if (not isinstance(data, dict)):
        print("data format error, expected dict: ", data)
        raise SystemExit

    if (data["symbol"] != args.symbol):
        print("returned data is not what we requested: ", data["symbol"], " != ", args.symbol)
        raise SystemExit
    
    return data

def log_data(data={}):
    last_time = datetime.fromisoformat(data["last_time"])
    date = last_time.date()

    log_directory = Path('logs')
    log_directory.mkdir(exist_ok=True)

    current_day_logfile_name = os.path.join(log_directory, "-".join((args.symbol, date.strftime("%Y%m%d"))))

    try:
        mod_time = datetime.fromtimestamp(os.path.getmtime(current_day_logfile_name), timezone.utc)
    except FileNotFoundError as e:
        # ignore the file not found, we fake a timestamp for the last used
        mod_time = datetime.fromtimestamp(0, timezone.utc)

    if (not args.no_log and last_time > mod_time):
        logging.basicConfig(
            filename=current_day_logfile_name, format="%(message)s", level=logging.INFO
        )
        logging.info(json.dumps(data, sort_keys=True))

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(prog='query-stock', description='Log the currently available stock price')
    parser.add_argument('-s', '--symbol', default='.SPX', help='stock ticker symbol (default: .SPX)')
    parser.add_argument('-nl', '--no_log', action='store_true', default=False, help='Suppress writing the stock price to a log file, outputs to stdout (default: False)')
    args = parser.parse_args()

    data = get_data(args.symbol)
    if (not args.no_log):
        log_data(data)
    else:
        print(json.dumps(data, sort_keys=True, indent=4))

