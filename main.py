import os
import sys
import copy
import math
import numpy
import time
import common
import random
import string
import requests
import subprocess

import pandas               as pd
import matplotlib.pyplot    as plt
import streamlit            as st
import plotly.express       as px
import pandas_ta            as pandas_ta
import vectorbt             as vbt

from io                     import StringIO
from datetime               import datetime
from tvDatafeed             import TvDatafeed, Interval
    
pd.set_option('expand_frame_repr', False)

STATE = False 
N_BARS = 50000

USERNAME = 'tradingpro.112233@gmail.com'
PASSWORD = 'Vuatrochoi123'

try:    
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
except Exception as e:
    st.write(e)

st.set_page_config(page_title = "QM Capital LLC", layout = "wide")
st.header("Stock Portfolio Optimizer")

col00, col01, col02, col03, col04 = st.columns(5)
with col00:
    data_tpye = st.selectbox('Select Data Type:',("Trading View", "Option No.2"))
    
with col01:
    ind_time_interval = st.selectbox('Select Time Interval:',("1 Minute", "3 Minutes", "5 Minutes", "15 Minutes", "30 Minutes", \
                                                            "45 Minutes", "1 Hour", "2 Hours", "3 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"))
with col02:
    tv_symbol = st.text_input("Symbol: (DCM)", "DCM")
with col03:
    tv_exchange = st.text_input("Exchange: (HOSE)", "HOSE")
with col04:
    st.text('')
    st.text('')
    but_01 = st.button("Show Data")     


if data_tpye == "Trading View":
    try:
        time_interval = common.return_time(ind_time_interval)
        st.session_state.DATA_TV = st.session_state.TRADINGVIEW.get_hist(symbol=tv_symbol, exchange=tv_exchange, interval=time_interval, n_bars=N_BARS) 
    except Exception as e:
        st.write(e)
try:
    st.session_state.DATA_TV.ta.cdl_pattern(name="all", append=True)
except Exception as e:
    st.write(e)

try:
    if but_01:
        st.session_state.BUT_01_STATE = True
    if st.session_state.BUT_01_STATE:
        st.write(st.session_state.DATA_TV)
except Exception as e:
    st.write(e)
CHAR = '"'
customA = st.text_area('Set CustomA: ({"kind": "macd", "fast": 12, "slow": 26})', placeholder = f"ALWAYS USE {CHAR} DO NOT USE ' IN BOX")
try: 
    if st.button("Set CustomA"):
        st.session_state.CustomA = customA
        st.write(common.cus_str2json(customA))
        custom_a = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customA))
        st.session_state.DATA_TV.ta.strategy(custom_a) 

        st.session_state.BUT_CUSTOMA = True
except Exception as e:
    st.write(e)

try:
    if st.session_state.BUT_CUSTOMA:
        st.write(st.session_state.DATA_TV)
except Exception as e:
    st.write(e)

customB = st.text_area('Set CustomB: ({"kind": "increasing", "strict": df[' + 'STOCHRSId_14_14_3_3' + '], "length": 10})', placeholder = f"ALWAYS USE {CHAR} DO NOT USE ' IN BOX")
try:
    if st.button("Set CustomB"):
        st.session_state.CustomB = customB
        st.write(common.cus_str2json(customB))
        custom_b = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customA))
        st.session_state.DATA_TV.ta.strategy(custom_b)
        st.session_state.BUT_CUSTOMB = True
except Exception as e:
    st.write(e)

try:
    if st.session_state.BUT_CUSTOMB:
        st.write(st.session_state.DATA_TV) 
        st.write(st.session_state.DATA_TV.columns.values)
except Exception as e:
    st.write(e)

col50, col51 = st.columns(2)
with col50:
    txt_entries = st.text_area("Set Entries: ( df['STOCHk_5_3_3'] > 80 ) + (df['EMA_10']< df['EMA_20'])", placeholder = "Logic input with variable 'df'", height=170)
    txt_exist   = st.text_area("Set Exist: (((df['EMA_10']< df['EMA_20']) & ( df['SUPERTd_7_3.0'] ==-1)))", placeholder = "Logic input with variable 'df'", height=170)
with col51:
    sl_stop     = float(st.text_input("SL Stop: (0.03)", "0.03"))
    sl_trail    = st.selectbox('SL Trail:', [True, False]) 
    tp_stop     = float(st.text_input("TP Stop: (0.03)", "0.03"))
    fees        = float(st.text_input("Fees: (0.00)", "0.00"))
    freq        = st.text_input("Freq:", "1d") 

try:
    if st.button("Set Entries/Exist/SL/TP/FEE/FREQ..."):
        df = st.session_state.DATA_TV
        new_entr = common.logic_str2json(txt_entries, 'st.session_state.DATA_TV')
        try:
            entries = eval(new_entr)
        except:
            entries = True
        new_exi = common.logic_str2json(txt_exist, 'st.session_state.DATA_TV')
        try:
            exists = eval(new_exi)        
        except:
            exists = True
        bt_pf = vbt.Portfolio.from_signals(st.session_state.DATA_TV, entries, exists,  direction='shortonly', accumulate='addonly',  sl_stop= sl_stop, sl_trail=sl_trail, tp_stop = tp_stop, fees=fees, freq= freq)
        st.write(bt_pf.stats())
        bt_pf.plot().show()
        bt_pf.plot_drawdowns().show()
        bt_pf.plot_trades().show()
except Exception as e:
    st.write(e)

try:
    pass

except Exception as e:
    st.write(e)
