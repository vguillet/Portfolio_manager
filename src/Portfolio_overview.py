
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
from datetime import datetime

# Libs
import pandas
import matplotlib.pyplot as plt

# Own modules
from Progress_bar_tool import Progress_bar
from src.Data_Collection_preparation.Data_processor import Data_processor
from src.Tools.PDF import PDF

from src.Tools.Plot_tools import Plot_tools


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Portfolio_overview:
    def __init__(self, fast_compile=False):
        # ======================== INITIALISATION =======================================
        # ----- Save settings
        self.fast_compile = fast_compile

        # ----- Initiate tools
        self.plot_tools = Plot_tools()

        # ----- Record date and time
        self.overview_timestamp = datetime.now()

        # ----- Run data processor
        self.data_processor = Data_processor()

        # ======================== OVERVIEW GENERATION ==================================
        # ----- Create Overview pdf
        self.pdf = PDF(orientation='P', unit='mm', format='A4')
        self.pdf.build_layout()

        # ----- Add pages
        pdf_compilation_progressbar = Progress_bar(max_step=6, label="PDF compilation")
        self.cover_page()

        pdf_compilation_progressbar.update_progress(current_process_label="Summary page")
        self.summary_page()

        pdf_compilation_progressbar.update_progress(current_process_label="Bitcoin page")
        self.bitcoin_page()

        pdf_compilation_progressbar.update_progress(current_process_label="Cardano page")
        self.cardano_page()

        pdf_compilation_progressbar.update_progress(current_process_label="Ethereum page")
        self.ethereum_page()

        pdf_compilation_progressbar.update_progress(current_process_label="Trade history page")
        self.trade_history_page()

        # ----- Export pdf
        self.export_pdf()

        return

    # ================================================================================================
    def cover_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        self.pdf.adjust_space(30)
        self.pdf.add_chapter("Portfolio overview: " + self.overview_timestamp.strftime("%Y-%m-%d"), align="C")
        self.pdf.add_floating_image("Data/Figures/Cover_image.png", self.pdf.x_margin, 100, width=self.pdf.text_width)
        self.pdf.add_textbox("Victor Guillet", 150, 235)

        return

    def summary_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        self.pdf.add_title("Portfolio Summary")

        self.pdf.add_subtitle("Investments recap")

        self.pdf.add_text("Total invested: " + str(round(self.data_processor.data_synthesis["Total"]["Invested"], 3)) + " eur")
        self.pdf.add_textbox("Assets worth: " + str(round(self.data_processor.timeline_data["portfolio_value_total"].iloc[-1])) + " eur", 80, 27.5)
        self.pdf.add_textbox("Percentage difference: " + str(round(self.data_processor.data_synthesis["Total"]["Percentage_difference"])) + " %", 140, self.pdf.y_tracker - 12.5)
        self.pdf.add_textbox("Net: " + str(round(self.data_processor.timeline_data["portfolio_value_" + "total"].iloc[-1] - self.data_processor.data_synthesis["Total"]["Invested"], 3)) + " eur", 140, self.pdf.y_tracker - 17.5)

        self.pdf.adjust_space(5)
        self.pdf.add_text("Transaction count: " + str(round(self.data_processor.data_synthesis["Total"]["Transaction_count"], 3)))
        self.pdf.add_text("Total fees: " + str(round(self.data_processor.data_synthesis["Total"]["Fee"], 3)) + " eur")

        if not self.fast_compile:
            self.plot_tools.plot_pie_chart(self.data_processor.trading_history_data, "cost",
                                           show_plot=False)
            self.pdf.add_floating_image("Data/~temp/cost_piechart.png", 20, 150, width=170)

        self.pdf.add_line(67.5)

        # self.pdf.add_subtitle("Performance overview")

        if not self.fast_compile:
            self.plot_tools.plot_portfolio_overview(self.data_processor.timeline_data, "total", "EUR",
                                                    show_plot=False)
            self.pdf.add_image("Data/~temp/" + "Portfolio_performance_" + "total" + "_linechart.png",
                               width=self.pdf.text_width + 10)

        if not self.fast_compile:
            self.pdf.add_page()
            self.pdf.reset_layout()

            counter = 0
            for pair in self.data_processor.traded_pairs:
                counter += 1
                if counter > 3:
                    counter = 1
                    self.pdf.add_page()
                    self.pdf.reset_layout()

                self.pdf.add_subsubtitle(pair[:-3] + "-" + pair[-3:])
                self.pdf.add_text("- Invested: " + str(round(self.data_processor.data_synthesis[pair]["Invested"], 3)) + " eur")
                self.pdf.add_text("- Volume: " + str(round(self.data_processor.data_synthesis[pair]["Volume"], 3)) + " " + pair[:-3])
                self.pdf.add_text("- APP: " + str(round(self.data_processor.data_synthesis[pair]["APP"], 3)) + " eur")
                self.pdf.add_textbox("Assets worth: " + str(round(self.data_processor.timeline_data["portfolio_value_" + pair].iloc[-1])) + " eur", 80, self.pdf.y_tracker - 27.5)
                self.pdf.add_textbox("Percentage difference: " + str(round(self.data_processor.data_synthesis[pair]["Percentage_difference"])) + " %", 140, self.pdf.y_tracker - 27.5)
                self.pdf.add_textbox("Net: " + str(round(self.data_processor.timeline_data["portfolio_value_" + pair].iloc[-1] - self.data_processor.data_synthesis[pair]["Invested"], 3)) + " eur", 140, self.pdf.y_tracker - 22.5)

                self.pdf.adjust_space(2)

                self.plot_tools.plot_portfolio_overview(self.data_processor.timeline_data, pair, pair[-3::],
                                                        width=800, height=300,
                                                        show_plot=False)
                self.pdf.add_image("Data/~temp/" + "Portfolio_performance_" + pair + "_linechart.png",
                                   width=self.pdf.text_width)
                self.pdf.adjust_space(55)

                if counter < 3:
                    self.pdf.add_line(self.pdf.y_tracker + 3)

        return

    # ================================================================================================
    def bitcoin_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        pair = "BTCEUR"
        pair_unit = " BTC"
        pair_name = "bitcoin"

        self.crypto_overview(pair_unit, pair_name)

        if not self.fast_compile:
            self.plot_tools.plot_candlestick_chart(self.data_processor.trading_pair_history_dict[pair],
                                                   pair[0:-3], pair[-3::],
                                                   show_plot=False)
            self.pdf.add_image("Data/~temp/" + pair[0:-3] + "-" + pair[-3::] + "_candlechart.png",
                               width=self.pdf.text_width + 10)

        self.pdf.adjust_space(75)

        self.pdf.add_subtitle("Summary")
        self.pdf.add_text("Bitcoin is a peer-to-peer online currency, meaning that all transactions happen directly between equal, independent network participants, without the need for any intermediary to permit or facilitate them. Bitcoin was created to allow 'online payments to be sent directly from one party to another without going through a financial institution'. Some concepts for a similar type of a decentralized electronic currency precede BTC, but Bitcoin holds the distinction of being the first-ever cryptocurrency to come into actual use.")
        self.pdf.adjust_space(30)
        self.pdf.add_text("Bitcoin's total supply is limited by its software and will never exceed 21,000,000 coins. New coins are created during the process known as 'mining': as transactions are relayed across the network, they get picked up by miners and packaged into blocks, which are in turn protected by complex cryptographic calculations. As compensation for spending their computational resources, the miners receive rewards for every block that they successfully add to the blockchain. At the moment of Bitcoin's launch, the reward was 50 bitcoins per block: this number gets halved with every 210,000 new blocks mined - which takes the network roughly four years. As of 2020, the block reward has been halved three times and comprises 6.25 bitcoins.")
        self.pdf.adjust_space(45)

        return

    def cardano_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        pair = "ADAEUR"
        pair_unit = " ADA"
        pair_name = "cardano"

        self.crypto_overview(pair_unit, pair_name)

        if not self.fast_compile:
            self.plot_tools.plot_candlestick_chart(self.data_processor.trading_pair_history_dict[pair],
                                                   pair[0:-3], pair[-3::],
                                                   show_plot=False)
            self.pdf.add_image("Data/~temp/" + pair[0:-3] + "-" + pair[-3::] + "_candlechart.png",
                               width=self.pdf.text_width + 10)

        self.pdf.adjust_space(75)

        self.pdf.add_subtitle("Summary")
        self.pdf.add_text("Cardano is a proof-of-stake blockchain platform that says its goal is to allow 'changemakers, innovators and visionaries' to bring about positive global change. The open-source project also aims to 'redistribute power from unaccountable structures to the margins to individuals' - helping to create a society that is more secure, transparent and fair. Cardano was founded back in 2017, and the ADA token is designed to ensure that owners can participate in the operation of the network. Because of this, those who hold the cryptocurrency have the right to vote on any proposed changes to the software.")
        self.pdf.adjust_space(35)
        self.pdf.add_text("Cardano was founded by Charles Hoskinson, who was also one of the co-founders of the Ethereum network. He is the CEO of IOHK, the company that built Cardano's blockchain.")
        self.pdf.adjust_space(10)
        self.pdf.add_text("Cardano is one of the biggest blockchains to successfully use a proof-of-stake consensus mechanism, which is less energy intensive than the proof-of-work algorithm relied upon by Bitcoin. The project has taken pride in ensuring that all of the technology developed goes through a process of peer-reviewed research, meaning that bold ideas can be challenged before they are validated. According to the Cardano team, this academic rigor helps the blockchain to be durable and stable - increasing the chance that potential pitfalls can be anticipated in advance.")
        self.pdf.adjust_space(30)

        return

    def ethereum_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        pair = "ETHEUR"
        pair_unit = " ETH"
        pair_name = "ethereum"

        self.crypto_overview(pair_unit, pair_name)

        if not self.fast_compile:
            self.plot_tools.plot_candlestick_chart(self.data_processor.trading_pair_history_dict[pair],
                                                   pair[0:-3], pair[-3::],
                                                   show_plot=False)
            self.pdf.add_image(r"Data\~temp/" + pair[0:-3] + "-" + pair[-3::] + "_candlechart.png",
                               width=self.pdf.text_width + 10)

        self.pdf.adjust_space(75)

        self.pdf.add_subtitle("Summary")
        self.pdf.add_text("Ethereum is a decentralized open-source blockchain system that features its own cryptocurrency, Ether. ETH works as a platform for numerous other cryptocurrencies, as well as for the execution of decentralized smart contracts.")
        self.pdf.adjust_space(15)
        self.pdf.add_text("Ethereum's own purported goal is to become a global platform for decentralized applications, allowing users from all over the world to write and run software that is resistant to censorship, downtime and fraud.")
        self.pdf.adjust_space(10)
        self.pdf.add_text("Ethereum has pioneered the concept of a blockchain smart contract platform. Smart contracts are computer programs that automatically execute the actions necessary to fulfill an agreement between several parties on the internet. They were designed to reduce the need for trusted intermediates between contractors, thus reducing transaction costs while also increasing transaction reliability.")
        self.pdf.adjust_space(20)
        self.pdf.add_text("In addition to smart contracts, Ethereum's blockchain is able to host other cryptocurrencies, called 'tokens,' through the use of its ERC-20 compatibility standard. In fact, this has been the most common use for the ETH platform so far: to date, more than 280,000 ERC-20-compliant tokens have been launched. Over 40 of these make the top-100 cryptocurrencies by market capitalization, for example, USDT, LINK and BNB.")
        self.pdf.adjust_space(30)

        return

    def crypto_overview(self, pair_unit, pair_name):
        if not self.fast_compile:
            self.pdf.add_floating_image("Data/Figures/" + pair_name.title() + "_logo.png", x_origin=160, y_origin=20, width=30)

        self.pdf.add_title(pair_name.title() + " -" + pair_unit)

        self.pdf.add_subtitle("Overview")
        self.pdf.add_text("Market cap rank: " + str(self.data_processor.market_stats[pair_name]['market_cap_rank']))
        self.pdf.add_text("Market cap: " + str(self.data_processor.market_stats[pair_name]['market_cap']) + " eur")
        self.pdf.adjust_space(5)
        self.pdf.add_text("Circulating supply: " + str(self.data_processor.market_stats[pair_name]['circulating_supply']) + pair_unit)

        if self.data_processor.market_stats[pair_name]['total_supply'] is not None:
            self.pdf.add_text("Total supply: " + str(self.data_processor.market_stats[pair_name]['total_supply']) + pair_unit)
        else:
            self.pdf.add_text("Total supply: Unlimited")

        self.pdf.add_textbox("Current price: " + str(self.data_processor.market_stats[pair_name]['current_price']) + " eur", 100, 39)
        self.pdf.add_textbox("All-time high: " + str(self.data_processor.market_stats[pair_name]['ath']) + " eur", 100, 49)
        self.pdf.add_textbox("All-time high date: " + str(self.data_processor.market_stats[pair_name]['ath_date'])[:10], 100, 54)
        return

    # ================================================================================================
    def trade_history_page(self):
        self.pdf.add_page()
        self.pdf.reset_layout()

        if not self.fast_compile:
            self.plot_tools.plot_dataframe(self.data_processor.trading_history_data, "Trading_history",
                                           show_plot=True)
            self.pdf.add_floating_image("Data/~temp/Trading_history_table.png",
                                        x_origin=27, y_origin=10,
                                        width=155)

        return

    def export_pdf(self):
        self.pdf.output("Portfolio_overview_" + self.overview_timestamp.strftime("%Y-%m-%d") + ".pdf", 'F')

        import webbrowser
        webbrowser.open_new(r"Portfolio_overview_" + self.overview_timestamp.strftime("%Y-%m-%d") + ".pdf")

        return

if __name__ == "__main__":
    overview = Portfolio_overview()
