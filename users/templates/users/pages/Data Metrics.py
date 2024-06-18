import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.vector_ar.vecm import VECM

# Page configuration
st.set_page_config(page_title="StockHive", page_icon=":1234:", layout="wide")

# Style component for justifying text
mystyle = '''
    <style>
        p {
            text-align: justify;
        }
    </style>
    '''

st.markdown(mystyle, unsafe_allow_html=True)

# Stock ticker data
ticker_dict = {
    "AAPL": "Apple Inc.",
    "GOOG": "Alphabet Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "FB": "Facebook Inc."
}

# Start and end date for stock data
yf.pdr_override()
startdate = datetime(2014,1,1)
enddate = datetime(2023,12,31)

with st.container():
    st.title("Data Metrics")
    st.write("---")

# User input
user_input = st.text_input("Enter Stock Ticker", 'AAPL')

# Fetching data
df = pdr.get_data_yahoo(user_input, start=startdate, end=enddate)

# Showing company name
if user_input in ticker_dict:
    st.markdown('**Company Name:**')
    st.text(ticker_dict[user_input])
else:
    st.markdown('**Company Name:**')
    st.text("Not in file")

# Showing stock data date range
st.markdown('**Date Range:**')
st.text("1st January, 2010 - 31st December, 2019")

# Describing data
st.markdown('**Data Description:**')
st.write(df.describe())

def calculate_rsi(data, periods=14):
    delta = data.diff()
    up = delta.where(delta > 0, 0.0)
    down = -delta.where(delta < 0, 0.0)
    
    # Calculate the exponential moving averages
    gain_ema = up.ewm(com=periods-1, min_periods=periods).mean()
    loss_ema = down.ewm(com=periods-1, min_periods=periods).mean()
    
    # Calculate the relative strength
    rs = gain_ema / loss_ema
    
    # Calculate the RSI
    rsi = 100.0 - (100.0 / (1.0 + rs))
    
    return rsi

def calculate_atr(data, window=14):
    # Calculate the true range
    data['TR'] = data[['High', 'Close']].max(axis=1) - data[['Low', 'Close']].min(axis=1)
    
    # Calculate the ATR
    data['ATR'] = data['TR'].rolling(window=window).mean()
    
    return data['ATR']

rsi = calculate_rsi(df['Close'], periods=14)

# RSI of data
st.markdown('**Relative Strength Index:**')
st.write("The RSI is a momentum indicator that measures the strength of a stock's price action. It is calculated by comparing the average gains to the average losses over a specified period of time, usually 14 days. The RSI ranges from 0 to 100, with readings above 70 indicating an overbought condition and readings below 30 indicating an oversold condition. Lets see the RSI values for last 30 days.")
st.text(rsi.tail(30))

# ATR of data
atr = calculate_atr(df, window=14)
st.markdown('**Average True Range:**')
st.write("The ATR measures the volatility of a stock's price action over a specified period of time. It is calculated by taking the average of the true range (the highest of the following: the difference between the high and low prices, the difference between the high and previous close, or the difference between the low and previous close) over a specified period of time. Lets see the ATR values for last 30 days.")
st.text(atr.tail(30))
