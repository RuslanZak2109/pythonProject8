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
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Page configuration
st.set_page_config(page_title="StockHive", page_icon=":1234:", layout="wide")

mystyle_sidebar = '''
    <style> .sidebar .sidebar-content { color: #ffffff; } </style>
'''
st.markdown(mystyle_sidebar, unsafe_allow_html=True)

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
    st.title("Data Visualizations")
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

# Line Graph
st.markdown('**Line Graph**')
fig = plt.figure(figsize = (12,6))
plt.xlabel("Time")
plt.ylabel("Close")
plt.plot(df.Close)
st.pyplot(fig)

# Histogram
st.markdown('**Histogram**')
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(df['Close'], bins=20)
ax.set_xlabel('Close')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# Heatmap
st.markdown('**Heatmap**')
returns = df.pct_change()
corr_matrix = returns.corr()
fig = plt.figure(figsize=(12, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
st.pyplot(fig)

# ACF and PACF
st.markdown('**ACF & PACF**')
close_df = df[['Close']]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
plot_acf(close_df, ax=ax1)
plot_pacf(close_df, ax=ax2)
st.pyplot(fig)
