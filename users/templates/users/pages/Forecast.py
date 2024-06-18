import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.vector_ar.vecm import VECM
from statsmodels.tsa.api import VAR

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
    "FB": "Facebook Inc.",
     "YNDX.ME": "Yandex Inc.",
    "V": "Visa Inc."

}

# Start and end date for stock data
yf.pdr_override()
startdate = datetime(2014,1,1)
enddate = datetime(2024,5,20)

with st.container():
    st.title("Forecast")
    st.write("---")

# User input
user_input = st.text_input("Enter Stock Ticker", 'AAPL')

# Fetching data
df = pdr.get_data_yahoo(user_input, start=startdate, end=enddate)
data = df.filter(['Open', 'Close'])

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

# Train-test split
df = df[['Close']]
train_data = df[:len(df)-100]
test_data = df[len(df)-100:]

# Model input
model_user_input = st.selectbox("Choose forecasting model", ("ARIMA", "AR", "MA"))

if(model_user_input == "ARIMA"):
    st.subheader("ARIMA")
    st.write("ARIMA, which stands for Autoregressive Integrated Moving Average, is a time series model used for forecasting future values of a variable based on its past values. ARIMA combines three different models: Autoregression (AR), Integration (I), and Moving Average (MA). The autoregressive component involves using past values of the time series to predict future values. The moving average component models the errors or residuals of the autoregressive component. The integrated component is used to remove any trends or seasonality in the time series data.")
    model_arima = sm.tsa.ARIMA(train_data, order=(2,0,2))
    model_arima_fit = model_arima.fit()
    forecast = model_arima_fit.forecast(steps=30)
    dates = pd.date_range(start=test_data.index[-1], periods=30, freq='D')
    forecast_df = pd.DataFrame({'Date': dates, 'Forecast': forecast})
    forecast_df = forecast_df.set_index('Date')
    st.markdown('**Predictions using ARIMA for next 30 days**')
    fig = plt.figure(figsize = (12,6))
    plt.plot(train_data, label='Training Data')
    plt.plot(test_data, label='Testing Data')
    plt.plot(forecast_df, label='Forecast')
    plt.legend()
    st.pyplot(fig)
    st.text(forecast_df)
elif(model_user_input == "AR"):
    st.subheader("AR")
    st.write("AR, which stands for Autoregressive, is a statistical model used for time series analysis and forecasting. In an AR model, the current value of a variable is predicted based on its past values. This means that the value of the variable at time t is a function of its past values at times t-1, t-2, t-3, and so on. The order of an AR model, denoted by p, indicates how many past values of the variable are used to predict the current value. For example, an AR(1) model uses only the previous value of the variable to make predictions, while an AR(2) model uses the previous two values.")
    model_ar = AutoReg(train_data, lags=4)
    model_ar_fit = model_ar.fit()
    forecast = model_ar_fit.forecast(steps=30)
    dates = pd.date_range(start=test_data.index[-1], periods=30, freq='D')
    forecast_df = pd.DataFrame({'Date': dates, 'Forecast': forecast})
    forecast_df = forecast_df.set_index('Date')
    st.markdown('**Predictions using AR for next 30 days**')
    fig = plt.figure(figsize = (12,6))
    plt.plot(train_data, label='Training Data')
    plt.plot(test_data, label='Testing Data')
    plt.plot(forecast_df, label='Forecast')
    plt.legend()
    st.pyplot(fig)
    st.text(forecast_df)
elif(model_user_input == "MA"):
    st.subheader("MA")
    st.write("MA, or Moving Average, is a statistical technique used to analyze time series data by calculating the average value of a set of data points over a specified period of time. The moving average is calculated by adding up the values of a set of data points and dividing by the number of data points in the set. The period of time used to calculate the moving average is called the window, and can be adjusted depending on the desired level of smoothing. MA is not a forecasting algorithm, but rather a tool used to smooth out data and identify trends. However, we can use the moving average to make a simple forecast by assuming that the future values will follow the same trend as the historical data.")
    data = df
    ma_data = data.rolling(window=30).mean()
    train_data_ma = ma_data.iloc[:len(ma_data)-100]
    test_data_ma = ma_data.iloc[len(ma_data)-100:]
    forecast = np.repeat(test_data_ma['Close'].iloc[-1], 30)
    dates = pd.date_range(start=test_data_ma.index[-1], periods=30, freq='D')
    forecast_df = pd.DataFrame({'Date': dates, 'Forecast': forecast})
    forecast_df = forecast_df.set_index('Date')
    fig = plt.figure(figsize = (12,6))
    plt.plot(train_data, label='Training Data')
    plt.plot(test_data, label='Testing Data')
    plt.plot(forecast_df, label='Forecast')
    plt.legend()
    st.pyplot(fig)
    st.text(forecast_df)


