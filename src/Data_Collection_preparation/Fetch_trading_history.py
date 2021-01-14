
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import os

# Libs
import pandas as pd

# Own modules
from PhyTrade.Data_Collection_preparation.Data_sources.Yahoo import pull_yahoo_data


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


def fetch_trading_history():
    path = r"Data\Trade_history\trades.csv"

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        data = pd.read_csv(path)

        # --> Remove unnecessary information
        del data["txid"]
        del data["ordertxid"]
        del data["margin"]
        del data["misc"]
        del data["ledgers"]

        # --> Format date
        data["time"] = data["time"].str[:10]

        # --> Rename trading pair
        data.loc[(data.pair == "XXBTZEUR"), "pair"] = "BTCEUR"
        data.loc[(data.pair == "XETHZEUR"), "pair"] = "ETHEUR"

        # --> Round values
        data = data.round(decimals=3)

        return data

    else:
        print("Trading history CSV does not exist")
        return None


if __name__ == "__main__":
    print(fetch_trading_history())
