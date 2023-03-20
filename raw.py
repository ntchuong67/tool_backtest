import pandas as pd
import numpy
from datetime import datetime
import math
import matplotlib.pyplot as plt
from tvDatafeed import TvDatafeed,Interval
import pandas_ta as pandas_ta
import talib
from stockstats import StockDataFrame
import vectorbt as vbt

pd.set_option('expand_frame_repr', False)

USERNAME = 'quangbac501@gmail.com'
PASSWORD = 'quangbac501'

def return_time(time):
    try:
       if time == "1h":
           return Interval.in_1_hour
       elif time =="15m":
           return Interval.in_15_minute
       elif time == "30m":
           return Interval.in_30_minute
       elif time == "1m":
           return Interval.in_1_minute
       elif time == "5m":
           return Interval.in_5_minute
       elif time == "4h":
           return Interval.in_4_hour
       elif time == "2h":
           return Interval.in_2_hour
       elif time == "3h":
           return Interval.in_3_hour
       elif time == "3m":
           return Interval.in_3_minute
       elif time == "45m":
           return Interval.in_45_minute
       elif time == "1d":
           return Interval.in_daily
       elif time == "1w":
           return Interval.in_weekly
       elif time == "1M":
           return Interval.in_monthly

    except:
        return "Unknown time format"
    
tv = TvDatafeed(USERNAME, PASSWORD)

# Get historical data
input_message = 'Symbol: '
symbol = str(input(input_message))
input_message = 'Exchange: '
exchange = str(input(input_message))

input_message = "Interval_time ['1m', '3m', '5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', '1d', '1w', '1M']"
interval_time = str(input(input_message)) # Edit to user can change
n_bars = 10000 # No of bars to download, max 5000. Defaults to 

if not symbol:
  symbol = 'DCM'
  
if not exchange:
  exchange = 'HOSE'
if not interval_time:
  interval_time = '4h'
interval_time = return_time(interval_time)
### Download from multi sources
print('-------------------')
print(f"Symbol: {symbol} - Exchange: {exchange}")
df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval_time, n_bars=n_bars)

# Data VN Index:
historical_vnindex_price_df = tv.get_hist(symbol='VNINDEX', exchange='HOSE', interval=interval_time, n_bars=n_bars)
#historical_us_price_df = tv.get_hist(symbol='tsla', exchange='NASDAQ', interval=interval_time, n_bars=n_bars)
row_count, column_count = df.shape
print(f"Download done with {row_count} rows and {column_count} columns")
print(df.values.tolist())

ohlc = df

custom_a = pandas_ta.Strategy(name="First Strategy", ta=[
    {"kind": "macd", "fast": 12, "slow": 26},
    {"kind": "supertrend", "length": 7, "multiplier": 3},
    {"kind": "macd", "fast": 20, "slow": 50},
    {"kind": "supertrend", "length": 14, "multiplier": 5},
    {"kind": "kdj", "length": 10},
    {"kind": "rsi", "length": 14 },
    {"kind": "sma", "length": 14  },
    {"kind": "ema","length": 20 },
    {"kind": "sma","length": 20 },
    {"kind": "ema","length": 25 },
    {"kind": "ema","length": 10 },
    {"kind": "stoch","k": 5, "d": 3, 'smooth':3 },
    {"kind": "ichimoku"},
    {"kind": "ha"},
    {"kind": "bbands", "length": 20},  
    {"kind": "stochrsi"}, 
    {"kind": "cmf","length": 21}])


#add indticators to dataframe
df.ta.strategy(custom_a)
#ADD candlestick
df.ta.cdl_pattern(name="all", append=True)

#Add custom indicators

custom_b = pandas_ta.Strategy(name="Second Strategy", ta=[
    {"kind": "increasing", "strict": "df['STOCHRSId_14_14_3_3']", "length": 10},
    {"kind": "sma", "strict": "df['volume']", "length": 5}])
df.ta.strategy(custom_b)


print(df)

entries = ( df['MACD_14_26_9'] > df['MACDs_14_26_9'] ) \
             & ( df['SUPERTd_7_3.0'] ==1 )
exist =  ( df['SUPERTd_7_3.0'] ==-1) 

bt_pf = vbt.Portfolio.from_signals(df['close'], entries, exist,  direction='shortonly', accumulate='addonly',  sl_stop= 0.03, sl_trail=True, tp_stop = 0.03, fees=0.00, freq= '1d')

print(bt_pf.stats())

bt_pf.plot().show()

bt_pf.plot_drawdowns().show()

bt_pf.plot_trades().show()