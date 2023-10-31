#!/usr/bin/env python
# coding: utf-8

# IMPORT LIBRARIES
import numpy as np
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import csv
import yfinance as yf

# READ THE FILE WITH STOCKS TO BE EXAMINED
# ATTENTION: STOCK CODES MUST USE YFINANCE FORMAT
tickers_df = pd.read_csv('stock_list.csv')
tickers_list = tickers_df['Tickers'].tolist()

# TIME DELTA. LAST 30 DAYS TO EXAMINE LAST WEEK CONDITIONS
today = datetime.now()
end = datetime(today.year, today.month, today.day)
start = end - timedelta(30)
date_index = pd.date_range(start, end, freq='D')

# CREATES AN EMPTY DATA FRAME
df_didi = pd.DataFrame()

# READS STOCK PRICES USING YFINANCE API - STOCKS LISTED ON stock_list.csv
for ticker in tickers_list:
    try:
        data = yf.download(ticker, start, end)
        adj_close = data['Adj Close']
        df_didi[ticker] = adj_close
        print(f"OK. Downloaded {ticker} prices.")
    except:
        print(f"FAIL to download {ticker} prices.")

# DEFINE LOGIC FOR "PERFECT NEEDLE" CASE AND RETURNS WHICH SIDE TO TRADE
def crossing_averages(MA3_list, MA20_list):
    crossed_above = False
    crossed_below = False
    for i in range(1, len(MA3_list) - 1):
        if MA3_list[i - 1] != 0 and MA20_list[i - 1] != 0 and MA3_list[i] != 0 and MA20_list[i] != 0:
            if MA3_list[i - 1] < 1 and MA20_list[i - 1] > 1 and MA3_list[i] >= 1 and MA20_list[i] <= 1:
                crossed_above = True
            elif MA3_list[i - 1] > 1 and MA20_list[i - 1] < 1 and MA3_list[i] <= 1 and MA20_list[i] >= 1:
                crossed_below = True

    if crossed_above:
        return "Buy"
    elif crossed_below:
        return "Sell"
    else:
        return "Nothing"

# CREATES THE MOVING AVERAGES ON EACH DATAFRAME (TICKER) AND PERFORMS THE CALCULATIONS
tickers = {}
try:
    for ticker in tickers_list:
        df = pd.DataFrame(index=date_index, columns=['price', 'MA3', 'MA20', 'dif_8_3', 'dif_20_8', 'didi', 'crossing'])
        df['price'] = df_didi[ticker]
        df = df.dropna(subset=['price'])

        df['MA3'] = df['price'].rolling(3).mean() / df['price'].rolling(8).mean()
        df['MA20'] = df['price'].rolling(20).mean() / df['price'].rolling(8).mean()
        df['dif_8_3'] = abs(1 - abs(df['MA3']))
        df['dif_20_8'] = abs(abs(df['MA20']) - 1)
        df['didi'] = (df['dif_8_3']) + (df['dif_20_8'])
        df.fillna(0, inplace=True)

        MA3_list = df['MA3'].tolist()
        MA20_list = df['MA20'].tolist()
        df['crossing'] = df.apply(lambda row: crossing_averages(MA3_list, MA20_list), axis=1)

        tickers[ticker] = df
except Exception as e:
    print(f"FAIL to process ticker {ticker}: {str(e)}")

# POPULATES THE LIST WITH STOCK NAME AND SIDE IN CASE OF "PERFECT NEEDLE"
# POPULATES THE LIST IN CASE OF "ATTENTION STOCKS", CONSIDERING "DIDI" EQUALS OR BELOW 0.005
tickers_with_signals = []
interesting_keys = []

for ticker, df in tickers.items():
    crossing_values = set(df[df['crossing'] != 'Nothing']['crossing'])
    
    # FILTER VALUES BELOW 0.005 AND NOT ZERO ON 'didi' COLUMN
    filtered_values = df[(df['didi'] <= 0.005) & (df['didi'] != 0)]
    
    # CHECK IF THERE ARE VALUES AFTER FILTERING
    if not filtered_values.empty:
        interesting_keys.append(ticker)
    
    if crossing_values:
        tickers_with_signals.append((ticker, crossing_values.pop()))

# OUTPUT
if not tickers_with_signals:
    print("**THERE'S NO PERFECT NEEDLE TODAY**")
else:
    print('**PERFECT NEEDLE**')
    print(tabulate(tickers_with_signals, headers=["STOCK", "SIDE"]))

if not interesting_keys:
    print("**NO STOCK REQUIRES ATTENTION**")
else:
    print("\nATTENTION STOCKS:")
for key in interesting_keys:
    print(key)
