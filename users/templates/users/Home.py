import requests
import streamlit as st

st.set_page_config(page_title="StockHive", page_icon=":1234:", layout="wide")

mystyle = '''
    <style>
        p {
            text-align: justify;
        }
    </style>
    '''

st.markdown(mystyle, unsafe_allow_html=True)

with st.container():
    st.title("StockHive")
    
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Welcome to StockHive")
        st.write("StockHive is a stock data forecasting and visualization webapp. It is mostly directed towards users who want to invest in the best stocks without much knowledge of the stock market, users such as beginners or simple hobby traders. The application utilizes advanced time series forecasting techniques on the stock data and produces predictions. It also visualizes the predictions using interactive dashboards and plots. The webapp is initially aimed for beginner, novice and hobby traders, but it can also be used by investors, financial analysts, professional traders who are interested in stock prices and making informed investment decisions.")
        st.markdown('<a href="/Forecast" target="_self">Go to Forecast</a>', unsafe_allow_html=True)
        #st.button('Go to forecasting')
    
    with right_column:
        st.write("")
