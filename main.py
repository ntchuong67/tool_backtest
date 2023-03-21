import os
import copy
import math
import numpy
import time
import common
import random
import string

import pandas               as pd
import matplotlib.pyplot    as plt
import streamlit            as st
import plotly.express       as px
import pandas_ta            as pandas_ta
import vectorbt             as vbt

from io                     import StringIO
from datetime               import datetime
from tvDatafeed             import TvDatafeed, Interval

if not os.path.isdir("/tmp/ta-lib"):
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("ls -la /app/equity/")
    # build
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    # install
    os.system("make install")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

pd.set_option('expand_frame_repr', False)

STATE = False 
N_BARS = 50000

USERNAME = 'quangbac501@gmail.com'
PASSWORD = 'quangbac501'

if "TRADINGVIEW" not in st.session_state:
    st.session_state.TRADINGVIEW = TvDatafeed(USERNAME, PASSWORD)
if "DATA_TV" not in st.session_state:
    st.session_state.DATA_TV = st.session_state.TRADINGVIEW.get_hist(symbol="DCM", exchange="HOSE", interval=Interval.in_1_minute, n_bars=N_BARS) 
if "BUT_01_STATE" not in st.session_state:
    st.session_state.BUT_01_STATE = False
if "BUT_CUSTOMA" not in st.session_state:
    st.session_state.BUT_CUSTOMA = False
if "CustomA" not in st.session_state:
    st.session_state.CustomA = ''
if "BUT_CUSTOMB" not in st.session_state:
    st.session_state.BUT_CUSTOMB = False
if "CustomB" not in st.session_state:
    st.session_state.CustomB = ''

st.set_page_config(page_title = "QM Capital LLC", layout = "wide")
st.header("Stock Portfolio Optimizer")

col00, col01, col02, col03, col04 = st.columns(5)
with col00:
    data_tpye = st.selectbox('Select Data Type:',("Trading View", "Option No.2"))
    
with col01:
    ind_time_interval = st.selectbox('Select Time Interval:',("1 Minute", "3 Minutes", "5 Minutes", "15 Minutes", "30 Minutes", \
                                                            "45 Minutes", "1 Hour", "2 Hours", "3 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"))
with col02:
    tv_symbol = st.text_input("Symbol:", "DCM")
with col03:
    tv_exchange = st.text_input("Exchange:", "HOSE")
with col04:
    st.text('')
    st.text('')
    but_01 = st.button("Show Data")     


if data_tpye == "Trading View":
    time_interval = common.return_time(ind_time_interval)
    st.session_state.DATA_TV = st.session_state.TRADINGVIEW.get_hist(symbol=tv_symbol, exchange=tv_exchange, interval=time_interval, n_bars=N_BARS) 

st.session_state.DATA_TV.ta.cdl_pattern(name="all", append=True)

if but_01:
    st.session_state.BUT_01_STATE = True

if st.session_state.BUT_01_STATE:
    st.write(st.session_state.DATA_TV)

customA = st.text_area('Set CustomA:', placeholder = "Type something")
if st.button("Set CustomA"): 
    st.session_state.CustomA = customA
    st.write(common.cus_str2json(customA))
    custom_a = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customA))
    st.session_state.DATA_TV.ta.strategy(custom_a) 

    st.session_state.BUT_CUSTOMA = True

if st.session_state.BUT_CUSTOMA:
    st.write(st.session_state.DATA_TV)

customB = st.text_area('Set CustomB:', placeholder = "Type something")
if st.button("Set CustomB"):
    st.session_state.CustomB = customB
    st.write(common.cus_str2json(customB))
    custom_b = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customA))
    st.session_state.DATA_TV.ta.strategy(custom_b)
    st.session_state.BUT_CUSTOMB = True

if st.session_state.BUT_CUSTOMB:
    st.write(st.session_state.DATA_TV)
    st.write(st.session_state.DATA_TV.columns.values)

col50, col51 = st.columns(2)
with col50:
    entries = st.text_area('Set Entries:', placeholder = "Type something", height=170)
    exist   = st.text_area('Set Exist:', placeholder = "Type something", height=170)
with col51:
    sl_stop     = st.text_input("SL Stop:", "0,03")
    sl_trail    = st.selectbox('SL Trail:', ["True", False])
    tp_stop     = st.text_input("TP Stop:", "0.03")
    fees        = st.text_input("Fees:", "0.00")
    freq        = st.text_input("Freq:", "1d") 

if st.button("Set Entries/Exist/SL/TP/FEE/FREQ..."):
    st.write("RUN COMMAN AND EXITS")
    # bt_pf = vbt.Portfolio.from_signals(df['close'], entries, exist,  direction='shortonly', accumulate='addonly',  sl_stop= 0.03, sl_trail=True, tp_stop = 0.03, fees=0.00, freq= '1d')
    # print(bt_pf.stats())
    # bt_pf.plot().show()
    # bt_pf.plot_drawdowns().show()
    # bt_pf.plot_trades().show()

try:
    pass

except Exception as e:
    st.write(e)
