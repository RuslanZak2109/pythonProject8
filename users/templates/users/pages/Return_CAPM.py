import datetime as dt
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as pdr
import CAPM_charts as graphs
import price_normalize as pn
import returns


st.set_page_config(page_title="CAPM",
                   page_icon=":moneybag:",layout="wide")

st.title("Capital Asset Pricing Model ")
st.caption("Модель оценки капитальных активов (CAPM) описывает взаимосвязь между систематическим риском, или общими опасностями инвестирования, и ожидаемой доходностью активов, в частности акций.Это финансовая модель, которая устанавливает линейную зависимость между требуемой доходностью инвестиций и риском.")
st.subheader("предполагаемый доход без риска = 4.5%")
#Inputs

col1,col2=st.columns([1,1])
col3,col4 = st.columns([1,1])
with col1:
    stock_list = st.multiselect("Выбирайте акции по тикеру",('AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'META', 'GOOG', 'BRK', 'UNH', 'XOM', 'JNJ', 'JPM', 'V', 'LLY', 'AVGO', 'PG', 'MA', 'HD', 'MRK', 'CVX', 'PEP', 'COST', 'ABBV', 'KO', 'ADBE', 'WMT', 'MCD', 'CSCO', 'PFE', 'CRM', 'TMO', 'BAC', 'NFLX', 'ACN', 'A','DE', 'GS', 'ELV', 'LMT', 'AXP', 'BLK', 'SYK', 'BKNG', 'MDLZ', 'ADI', 'TJX', 'GILD', 'MMC', 'ADP', 'VRTX', 'AMT', 'C', 'CVS', 'LRCX', 'SCHW', 'CI', 'MO', 'ZTS', 'TMUS', 'ETN', 'CB', 'FI','GAZP.ME','SBER.ME','LKOH.ME','YNDX.ME','MGNT.ME'),('AAPL','TSLA','AMZN','GOOGL'))
with col2:
    year = st.number_input("Количество лет",1,10)

#download s&p data form fred using pdr
try:
    end=dt.date.today()
    start = dt.date(end.year-year,end.month,end.day)

    sp500_data= pdr.DataReader(['sp500'],'fred',start,end)

    #new data frame to store the close data according to date
    stocks_df = pd.DataFrame()

    for stock in stock_list:
        data = yf.download(stock,period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']


    #Preparing for Transformation
    stocks_df.reset_index(inplace=True)
    sp500_data.reset_index(inplace=True)
    sp500_data.columns = ['Date','sp500']
    stocks_df["Date"] = stocks_df["Date"].astype("datetime64[ns]")
    stocks_df['Date'] = stocks_df["Date"].apply(lambda x:str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df["Date"])


    #merging data
    stocks_df = pd.merge(stocks_df,sp500_data, on ='Date', how ="inner")

    #show dataframe head
    with col1:  
        st.markdown("### Stock Prices (Head)")
        st.dataframe(stocks_df.head(),use_container_width=True,width=2000,hide_index=True)
    with col2: 
        st.markdown("### Stock Prices (Tail) ")
        st.dataframe(stocks_df.tail(),use_container_width=True,hide_index=True)
    #show graph normalized graph comparison
    with col1: 
        st.markdown("### Normalized Prices")
        st.caption("Цены нормализуются по сравнению с первоначальными ценами на акции")
        stocks_df_normalized = pn.normalized(stocks_df)
        st.plotly_chart(graphs.interactive_plot(stocks_df_normalized))

    #daily returns and CAPM returns
    stocks_daily_return = returns.daily_returns(stocks_df)

    #calculate beta

    beta={}
    alpha={}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i !='sp500':
            b,a = returns.beta(stocks_daily_return, i)
            beta[i]=b
            alpha[i]=a

    beta_df = pd.DataFrame(columns=["Stock","Beta Value"])
    beta_df["Stock"] =beta.keys()
    beta_df["Beta Value"] = [str(round(i,2)) for i in beta.values()]

    with col3:  
        st.markdown("### Рассчитанный риск")
        st.caption("рыночный риск рассматривается как 1")
        st.dataframe(beta_df,use_container_width=True,hide_index=True)

    risk_free_asset = 4.5
    market_return = stocks_daily_return["sp500"].mean()*252  #252 is the number of active trading days

    return_df = pd.DataFrame()
    return_value = []
    for stock, value in beta.items():
        return_value.append(str(round(risk_free_asset+(value*(market_return-risk_free_asset)),2)))
    return_df['Stock'] = stock_list

    return_df['Return Value'] = return_value

    with col4:
        st.markdown("### Рассчитанный доход с использованием CAPM")
        st.caption("безрисковая ставка + бета (или риск) инвестиции * ожидаемая доходность на рынке - безрисковая ставка")
        st.dataframe(return_df,use_container_width=True,hide_index=True)
except:
    st.write("Пожалуйста, выберите по крайней мере 1 компанию")


hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)