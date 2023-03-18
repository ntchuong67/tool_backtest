import pandas as pd
import numpy

from datetime import datetime


import math
import matplotlib.pyplot as plt
#from tvDatafeed import TvDatafeed,Interval
import pandas_ta as pandas_ta
import talib
from stockstats import StockDataFrame
import vectorbt as vbt


import streamlit as st
import copy
import plotly.express as px


st.set_page_config(page_title = "Stock Portfolio Optimizer - developed by Nguyen Tien Chuong", layout = "wide")
st.header("Stock Portfolio Optimizer - developed by Nguyen Tien Chuong")

col0, col1, col2 = st.columns(3)
with col0:
    start_date = st.text_input("Start Date, e.g. 2018-01-01")
with col1:
    trial_date = st.text_input("End Traning Date, e.g. 2022-01-01")
with col2:
    end_date = st.text_input("End Date, e.g. 2023-02-01") # it defaults to current date

