
##################################################################################################################
"""

"""

# Built-in/Generic Imports
from datetime import datetime

# Libs
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI

# Own modules
from Progress_bar_tool import Progress_bar
from src.Data_Collection_preparation.Fetch_trading_history import fetch_trading_history
from src.Data_Collection_preparation.Fetch_trading_pair_history import fetch_trading_pair_history
from src.Data_Collection_preparation.Data_sources.coinAPI import pull_coinAPI_data


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Data_processor:
    def __init__(self):
        # ----- Initiate records
        self.data_synthesis = {}
        self.trading_pair_history_dict = {}
        self.market_stats = {}
        self.timeline_data = pd.DataFrame()

        # ----- Fetch and prepare data
        # --> Fetch trading history
        self.trading_history_data = fetch_trading_history()

        # --> Fetch historical data for asset pair in trading history
        self.traded_pairs = set(self.trading_history_data["pair"].tolist())

        api_call_progressbar = Progress_bar(max_step=4, label="Historical data download")

        for i, pair in enumerate(self.traded_pairs):
            api_call_progressbar.update_progress(current=i, current_process_label=pair)

            # --> Call api
            timeseries = pull_coinAPI_data(pair[0:-3], counter_value=pair[-3::])

            # --> Read csv
            # timeseries = fetch_trading_pair_history(pair[0:-3], counter_value=pair[-3::])

            self.trading_pair_history_dict[pair] = timeseries
            if "date" not in self.timeline_data.columns.values:
                self.timeline_data["date"] = timeseries["time_close"]

            self.timeline_data[pair] = timeseries["price_close"]

        # --> Fetch market data
        coins = {"BTC": "bitcoin",
                 "ADA": "cardano",
                 "ETH": "ethereum",
                 "LINK": "chainlink",
                 "DOT": "polkadot"}

        ids = ""
        for pair in self.traded_pairs:
            ids += coins[pair[:-3]] + ","
        ids = ids[:-1]

        market_lst = CoinGeckoAPI().get_coins_markets(ids=ids, vs_currency='eur')

        for pair in market_lst:
            self.market_stats[pair["id"]] = pair

        # ----- Perform data analysis
        self.create_portfolio_timeline()
        self.create_data_synthesis()

    def create_portfolio_timeline(self):
        portfolio_timeline_value = {}

        for pair in self.traded_pairs:
            portfolio_timeline_value[pair] = {"cumulated_volume": [],
                                              "cumulated_invested": [],
                                              "date": []}

            cumulated_volume_tracker = 0
            cumulated_invested_tracker = 0
            for index, row in self.trading_history_data.iterrows():
                if row["pair"] == pair:
                    cumulated_volume_tracker += row["vol"]
                    cumulated_invested_tracker += row["cost"]

                    portfolio_timeline_value[pair]["cumulated_volume"].append(cumulated_volume_tracker)
                    portfolio_timeline_value[pair]["cumulated_invested"].append(cumulated_invested_tracker)

                    portfolio_timeline_value[pair]["date"].append(row["time"])

            self.timeline_data["portfolio_volume_" + pair] = np.nan
            self.timeline_data["portfolio_invested_" + pair] = np.nan
            self.timeline_data["portfolio_value_" + pair] = np.nan

            cumulated_volume_tracker = 0
            cumulated_invested_tracker = 0
            for i, row in self.timeline_data.iterrows():
                if row["date"] in portfolio_timeline_value[pair]["date"]:
                    cumulated_volume_lst = []
                    cumulated_invested_lst = []

                    # Find index of all cumulated values matching date
                    for index in [i for i, e in enumerate(portfolio_timeline_value[pair]["date"]) if e == row["date"]]:
                        cumulated_volume_lst.append(portfolio_timeline_value[pair]["cumulated_volume"][index])
                        cumulated_invested_lst.append(portfolio_timeline_value[pair]["cumulated_invested"][index])

                    cumulated_volume_tracker = max(cumulated_volume_lst)
                    cumulated_invested_tracker = max(cumulated_invested_lst)

                # --> Update pair value
                self.timeline_data.at[i, "portfolio_volume_" + pair] = cumulated_volume_tracker
                self.timeline_data.at[i, "portfolio_invested_" + pair] = cumulated_invested_tracker
                self.timeline_data.at[i, "portfolio_value_" + pair] = cumulated_volume_tracker * row[pair]

            self.timeline_data.plot(x="date", y="portfolio_invested_" + pair)
            self.timeline_data.plot(x="date", y="portfolio_value_" + pair)

        self.timeline_data["portfolio_invested_total"] = np.nan
        self.timeline_data["portfolio_value_total"] = np.nan

        for i, row in self.timeline_data.iterrows():
            daily_invested_total = 0
            daily_value_total = 0
            for pair in self.traded_pairs:
                daily_invested_total += row["portfolio_invested_" + pair]
                daily_value_total += row["portfolio_value_" + pair]

            self.timeline_data.at[i, "portfolio_invested_total"] = daily_invested_total
            self.timeline_data.at[i, "portfolio_value_total"] = daily_value_total

        return

    def create_data_synthesis(self):
        self.data_synthesis = {"Total": {"Transaction_count": 0,
                                         "Invested": 0,
                                         "Value": round(self.timeline_data["portfolio_value_total"].iloc[-1]),
                                         "Fee": 0}}

        for index, row in self.trading_history_data.iterrows():
            self.data_synthesis["Total"]["Transaction_count"] += 1
            self.data_synthesis["Total"]["Fee"] += row["fee"]

            if row["type"] == "buy":
                self.data_synthesis["Total"]["Invested"] += row["cost"]

        self.data_synthesis["Total"]["Percentage_difference"] = (self.data_synthesis["Total"]["Value"] - self.data_synthesis["Total"]["Invested"])/self.data_synthesis["Total"]["Invested"] * 100

        for pair in self.traded_pairs:
            self.data_synthesis[pair] = {"Transaction_count": 0,
                                         "Volume": 0,
                                         "Invested": 0,
                                         "Value": round(self.timeline_data["portfolio_value_" + pair].iloc[-1]),
                                         "PP_lst": [],
                                         "Fee": 0}

            for index, row in self.trading_history_data.iterrows():
                if row["pair"] == pair:
                    if row["type"] == "buy":
                        self.data_synthesis[pair]["Transaction_count"] += 1
                        self.data_synthesis[pair]["Volume"] += row["vol"]
                        self.data_synthesis[pair]["Invested"] += row["cost"]
                        self.data_synthesis[pair]["PP_lst"].append(row["price"])
                        self.data_synthesis[pair]["Fee"] += row["fee"]

                if self.data_synthesis[pair]["Transaction_count"] > 0:
                    self.data_synthesis[pair]["APP"] = sum(self.data_synthesis[pair]["PP_lst"]) / \
                                                       self.data_synthesis[pair]["Transaction_count"]

            self.data_synthesis[pair]["Percentage_difference"] = (self.data_synthesis[pair]["Value"] - self.data_synthesis[pair]["Invested"]) / self.data_synthesis[pair]["Invested"] * 100

        return
