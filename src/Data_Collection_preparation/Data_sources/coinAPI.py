
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import requests

# Libs
import pandas as pd
from datetime import datetime

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

#################################################################################################################


def pull_coinAPI_data(currency, counter_value="EUR"):
    # --> Connect using API and fetching requested ticker data
    api_key = "081DB536-C237-4344-9A5C-2DEDC5931EA0"

    # --> Set start and end date of query
    start_date = datetime(2020, 6, 1, 0, 0, 0)
    end_date = datetime.now()

    # --> Construct request url
    url = "https://rest.coinapi.io/v1/ohlcv/" + currency + "/" + counter_value + "/history?period_id=1DAY&" + \
          "time_start=" + start_date.strftime("%Y-%m-%d") + "T00:00:00&" + \
          "time_end=" + end_date.strftime("%Y-%m-%d") + "T23:59:00&limit=100000"

    headers = {"X-CoinAPI-Key": api_key}

    # --> Perform request
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        # API response
        print("Too many requests.")

    # --> Format response to json
    response_data = json.loads(response.text)

    # --> Format json to pandas dataframe
    data = pd.DataFrame(response_data)

    # --> Remove unnecessary information
    del data["time_period_start"]
    del data["time_period_end"]
    del data["trades_count"]

    # --> Round values
    data = data.round(decimals=3)

    # --> Format date
    data["time_open"] = data["time_open"].str[:10]
    data["time_close"] = data["time_close"].str[:10]

    # --> Save data to csv
    data.to_csv("Data/Pair_historical_data/" + currency + "-" + counter_value + "_historical_data.csv", index=True)

    return data


if __name__ == "__main__":
    pull_coinAPI_data("XXBTZ")
