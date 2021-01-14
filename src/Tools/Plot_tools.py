
##################################################################################################################
"""

"""

# Built-in/Generic Imports
from datetime import datetime

# Libs
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

#################################################################################################################


class Plot_tools:
    def __init__(self):
        pd.options.plotting.backend = "plotly"

    @staticmethod
    def plot_portfolio_overview(data, pair, counter_value, width=800, height=380, show_plot=False):
        fig = data.plot(x="date", y=["portfolio_invested_" + pair, "portfolio_value_" + pair])

        fig.update_layout(title="Portfolio performance - " + pair.title(), title_x=0.5,
                          yaxis_title=counter_value,
                          autosize=False,
                          width=width,
                          height=height)

        if show_plot:
            fig.show()

        fig.write_image("Data/~temp/Portfolio_performance_" + pair + "_linechart.png")

        return

    @staticmethod
    def plot_candlestick_chart(data, currency, counter_value, width=800, height=380, show_plot=False):
        # --> Create figure
        fig = go.Figure(data=[go.Candlestick(x=data['time_close'],
                                             open=data['price_open'], close=data['price_close'],
                                             high=data['price_high'], low=data['price_low'], )])

        fig.update_layout(
                          title=currency + "-" + counter_value, title_x=0.5,
                          yaxis_title=counter_value,
                          autosize=False,
                          width=width,
                          height=height)

        if show_plot:
            fig.show()

        # --> Remove range slider before converting to image
        fig.update_layout(xaxis_rangeslider_visible=False)

        fig.write_image("Data/~temp/" + currency + "-" + counter_value + "_candlechart.png")

        return

    @staticmethod
    def plot_pie_chart(data, values="cost", show_plot=False):
        fig = px.pie(data, values=values, names="pair")
        fig.update_traces(textposition='inside', textinfo='percent+label')

        fig.update_layout(title=values.title() + " allocation", title_x=0.5,
                          showlegend=False)

        if show_plot:
            fig.show()

        fig.write_image("Data/~temp/" + values + "_piechart.png")

        return

    @staticmethod
    def plot_dataframe(data, name, col_width=2.0, row_height=0.625, font_size=14,
                       header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                       bbox=[0, 0, 1, 1], header_columns=0,
                       ax=None, show_plot=False):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns)

        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])

        if show_plot:
            plt.show()

        ax.get_figure().savefig("Data/~temp/" + name + "_table.png")

        return
