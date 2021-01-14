
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


def fetch_trading_pair_history(currency, counter_value):
    path = "Data/Pair_historical_data/##-**_historical_data.csv"
    path = path.replace('\\', '/').replace('##', currency).replace('**', counter_value)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        data = pd.read_csv(path)

        return data

    else:
        print("Pair trading history CSV does not exist")
        return None

