import os
import sys 
import copy
import math
import numpy
import json
import time
import common
import random
import string
import requests
import subprocess

import talib
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
N_BARS = 20000

USERNAME = 'tradingpro.112233@gmail.com'
PASSWORD = 'Vuatrochoi123'

if "TRADINGVIEW" not in st.session_state:
    st.session_state.TRADINGVIEW = TvDatafeed(USERNAME, PASSWORD)

def load_data(file_name, sysb, excha, interv):
    if 0: #os.path.isfile(file_name):
        with open(file_name) as f:
            __data = json.load(f)
        _symbol = __data["symbol"]
        del __data["symbol"]
        pd_data = pd.DataFrame.from_dict(__data, orient ='index')
    else:        
        pd_data, _symbol = st.session_state.TRADINGVIEW.get_hist(symbol=sysb, exchange=excha, interval=interv, n_bars=N_BARS)

        # result  = pd_data.to_json(orient="index")
        # dictionary = json.loads(result) 
        # dictionary["symbol"] = _symbol
        # with open(file_name, "w") as outfile:
        #     json.dump(dictionary, outfile)
    pd_data.insert(0, "symbol", value=_symbol)
    return pd_data

try:                
    if "DATA_TV" not in st.session_state:
        st.session_state.DATA_TV = load_data('data/DCM_HOSE_1_Minute.json',"DCM","HOSE", Interval.in_1_minute)
    if "DATA_TV_OLD" not in st.session_state:
        st.session_state.DATA_TV_OLD = st.session_state.DATA_TV
    if "DATA_TV_ADD" not in st.session_state:
        st.session_state.DATA_TV_ADD = load_data('data/DCM_HOSE_1_Minute.json',"VN301!","hnx", Interval.in_1_minute).reset_index()
    if "BUT_01_STATE" not in st.session_state:
        st.session_state.BUT_01_STATE = False
    if "BUT_01_MERGE" not in st.session_state:
        st.session_state.BUT_01_MERGE = False
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
st.header("QM Capital Trading system")

col00, col01, col02, col03, col04 = st.columns(5)
with col00:
    data_tpye = st.selectbox('Select Data Type:',("Trading View", "FireAnt", "TCBS"))
with col01:
    tv_symbol = st.text_input("Symbol: (FPT)", "FPT")
with col02:
    tv_exchange = st.text_input("Exchange: (HOSE)", "HOSE")
with col03:
    ind_time_interval = st.selectbox('Select Time Interval:',("1 Minute", "3 Minutes", "5 Minutes", "15 Minutes", "30 Minutes", \
                                                            "45 Minutes", "1 Hour", "2 Hours", "3 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"))
with col04:
    st.text('')
    st.text('')
    but_01 = st.button("Load Data")     

col10, col11, col12, col13 = st.columns(4) 
with col10:
    tv_symbol_merge = st.text_input("Additional data (VN301!)", "VN301!")
with col11:
    tv_exchange_merge = st.text_input("Exchange: (hnx)", "hnx")
with col12:
    ind_time_interval_merge = st.selectbox('Time Interval:',("1 Minute", "3 Minutes", "5 Minutes", "15 Minutes", "30 Minutes", \
                                                            "45 Minutes", "1 Hour", "2 Hours", "3 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"))
with col13:
    st.text('')
    st.text('')
    but_merge = st.button("ADD Data")


if 1: #data_tpye == "Trading View":
    try:
        time_interval = common.return_time(ind_time_interval)
        time_interval_merge = common.return_time(ind_time_interval_merge)
    except Exception as e:
        st.write(e)

col20, col21 = st.columns(2)
try:
    if but_01:
        _fln = 'data/' + tv_symbol + '_' + tv_exchange + '_' + ind_time_interval.replace(' ', '_') + '.json'
        st.session_state.DATA_TV = load_data(_fln, tv_symbol, tv_exchange, time_interval)
        st.session_state.DATA_TV_OLD = st.session_state.DATA_TV
        st.session_state.BUT_01_STATE = True
    if st.session_state.BUT_01_STATE:
        with col20:
            st.write("Before Merge Data:")
            st.write(st.session_state.DATA_TV_OLD)
except Exception as e:
    st.write(e)

CHAR = '"'

try:
    if but_merge:
        _fln_merge = 'data/' + tv_symbol_merge + '_' + tv_exchange_merge + '_' + ind_time_interval_merge.replace(' ', '_') + '.json'
        st.session_state.DATA_TV_ADD = load_data(_fln_merge, tv_symbol_merge, tv_exchange_merge, time_interval_merge)#.reset_index()
        st.session_state.DATA_TV = st.session_state.DATA_TV.merge(st.session_state.DATA_TV_ADD, left_index=True, right_index=True) 
        st.session_state.DATA_TV = st.session_state.DATA_TV.rename(columns={"open_x": "open", "high_x": "high", "low_x": "low","close_x": "close","volume_x": "volume"})
        st.session_state.BUT_01_MERGE = True
    if st.session_state.BUT_01_MERGE:
        with col21:
            st.write("After Merge Data:")
            st.write(st.session_state.DATA_TV)
except Exception as e:
    st.write(e)

customA = st.text_area('Set indicators: {"kind": "macd", "fast": 12, "slow": 26}', placeholder = f"ALWAYS USE {CHAR} DO NOT USE ' IN BOX")

while 'df' in customA:
    _val = ''
    for i in range(customA.index('df'), len(customA)-1):
        _val += customA[i]
        if _val[-1] == ']': break

    _val = _val.replace('df', 'st.session_state.DATA_TV')
    z = customA.index('df') 
    customA = customA[:z] + str(eval(_val)) + customA[z+2:]

but_cusA = st.button("Load Indicators")
col30, col31 = st.columns(2)
try: 
    if but_cusA:
        st.session_state.CustomA = customA
        custom_a = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customA))
        st.session_state.DATA_TV.ta.strategy(custom_a)
        st.session_state.DATA_TV.ta.cdl_pattern(name="all", append=True)
        st.session_state.BUT_CUSTOMA = True

except Exception as e:
    st.write(e)

try:
    if st.session_state.BUT_CUSTOMA:
        with col30:
            st.write(common.cus_str2json(customA))
        with col31:
            st.write(st.session_state.DATA_TV)
except Exception as e:
    st.write(e)

customB = st.text_area('Set Customized Indicators: {"kind": "sma", "close": "volume", "length": 5, "prefix": "vol"}', placeholder = f"ALWAYS USE {CHAR} DO NOT USE ' IN BOX")
while 'df' in customB:
    _val = ''
    for i in range(customB.index('df'), len(customB)-1):
        _val += customB[i]
        if _val[-1] == ']': break

    _val = _val.replace('df', 'st.session_state.DATA_TV')
    z = customB.index('df')
    customB = customB[:z] + str(eval(_val)) + customB[z+2:]

butcusB = st.button("Load Customized Indicators")

colcusB01, colcusB02, colcusB03 = st.columns(3)
try:
    if butcusB:
        st.session_state.CustomB = customB
        custom_b = pandas_ta.Strategy(name="First Strategy", ta=common.cus_str2json(customB))
        st.session_state.DATA_TV.ta.strategy(custom_b)
        st.session_state.BUT_CUSTOMB = True
except Exception as e:
    st.write(e)

try:
    if st.session_state.BUT_CUSTOMB:
        with colcusB01:
            st.write(common.cus_str2json(customB))
        with colcusB02:
            st.write(st.session_state.DATA_TV) 
        with colcusB03:
            xxxx = st.session_state.DATA_TV.columns.values
            xxxx = xxxx.transpose()
            st.write(xxxx)
except Exception as e:
    st.write(e)

col50, col51 = st.columns(2)
with col50:
    txt_entries = st.text_area("Set Entries: ( df['STOCHk_5_3_3'] > 80 ) + (df['EMA_10']< df['EMA_20'])", placeholder = "Logic input with variable 'df'", height=212)
    txt_exist   = st.text_area("Set Exist: (((df['EMA_10']< df['EMA_20']) & ( df['SUPERTd_7_3.0'] ==-1)))", placeholder = "Logic input with variable 'df'", height=212)
with col51:
    direction   = st.text_input("Direction: (Option)#", "longonly")
    sl_stop     = float(st.text_input("Stop Loss (%)", "100"))/100
    sl_trail    = bool(st.selectbox('SL Trail:', [True, False]))
    tp_stop     = float(st.text_input("Taking profit (%)", "70"))/100
    fees        = float(st.text_input("Fees: (%)", "2.5"))/100
    freq        = st.text_input("Freq:", "1d") 

try:
    if st.button("Calculate Performance"):
        df = st.session_state.DATA_TV
        new_entr = common.logic_str2json(txt_entries, 'st.session_state.DATA_TV')
        try:
            entries = eval(new_entr) 
        except Exception as e:
            st.write(e)
            entries = None
        new_exi = common.logic_str2json(txt_exist, 'st.session_state.DATA_TV')
        try:
            exists = eval(new_exi)
        except Exception as e:
            st.write(e)
            exists = None
        bt_pf = vbt.Portfolio.from_signals(st.session_state.DATA_TV['close'], entries, exists,  direction=direction, accumulate='addonly',  sl_stop= sl_stop, sl_trail=sl_trail, tp_stop = tp_stop, fees=fees, freq= freq)
        st.write(bt_pf.stats())
        with st.container():
            colch1, colch2 = st.columns(2)
            with colch1:
                st.plotly_chart(bt_pf.plot())
            with colch2:
                st.plotly_chart(bt_pf.plot_drawdowns())
                st.plotly_chart(bt_pf.plot_trades())
except Exception as e:
    st.write(e)

try:
    pass

except Exception as e:
    st.write(e)
