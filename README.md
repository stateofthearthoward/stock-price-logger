# Stock Price Logger
This is just a sample program to show some capabilities of python and fake screen scraping. This is more of a API caller with some simple logging of the output.

    usage: query-stock [-h] [-s SYMBOL] [-nl]
    
    Log the currently available stock price
    
    options:
      -h, --help            show this help message and exit
      -s SYMBOL, --symbol SYMBOL
                            stock ticker symbol (default: .SPX)
      -nl, --no_log         Suppress writing the stock price to a log file, outputs to stdout (default: False)

If the `logs` folder doesn't exist, it is created. A log file is created for each new trading day.

Example output with no log (passing in `-nl` argument):

    {
        "EventData": {
            "is_halted": "N",
            "yrhiind": "N",
            "yrloind": "N"
        },
        "altName": "S&P 500 INDEX",
        "altSymbol": ".SPX",
        "change": "-49.48",
        "change_pct": "-1.19%",
        "changetype": "DOWN",
        "code": 0,
        "countryCode": "US",
        "curmktstatus": "REG_MKT",
        "currencyCode": "USD",
        "exchange": "INDEX",
        "feedSymbol": ".SPX",
        "high": "4,136.54",
        "issue_id": "593933",
        "last": "4,098.12",
        "last_time": "2023-02-16T15:39:45.000-0500",
        "last_timedate": "3:39 PM EST",
        "low": "4,091.07",
        "name": "S&P 500 Index",
        "onAirName": "S&P 500",
        "open": "4,114.75",
        "portfolioindicator": "N",
        "previous_day_closing": "4,147.60",
        "provider": "CNBC Quote Cache",
        "realTime": "true",
        "shortName": "S&P 500",
        "source": "Exchange",
        "streamable": "1",
        "subType": "Index",
        "symbol": ".SPX",
        "symbolType": "symbol",
        "timeZone": "EST",
        "type": "INDEX",
        "yrhidate": "03/29/22",
        "yrhiprice": "4,637.30",
        "yrlodate": "10/13/22",
        "yrloprice": "3,491.58"
    }
