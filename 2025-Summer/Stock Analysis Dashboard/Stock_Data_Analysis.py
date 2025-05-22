import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import talib
import datetime

def get_ticker_components():
    df_sp = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df_sp = df_sp[0]
    df_dx = pd.read_html("https://en.wikipedia.org/wiki/DAX")
    df_dx = df_dx[4]
    df_dx = df_dx.rename(columns={"Ticker": "Symbol", "Company": "Security"})
    df = pd.concat([df_sp,df_dx],axis=0,join="inner").sort_values("Security")
    tickers = df["Symbol"].to_list()
    tickers_companies_dict = dict(zip(df["Symbol"],df["Security"]))
    return tickers, tickers_companies_dict

indicators = [
    "Simple Moving Average",
    "Exponential Moving Average",
    "Relative Strength index"
]

def apply_indicator(indicator, data):
    if indicator == "Simple Moving Average":
        close_float = [float(x) for x in data.iloc[:,0]]
        close_price = np.array(close_float)
        sma = talib.SMA(close_price)
        return pd.DataFrame({"Close": data.iloc[:,0], "SMA": sma})
    elif indicator == "Exponential Moving Average":
        close_float = [float(x) for x in data.iloc[:,0]]
        close_price = np.array(close_float)
        ema = talib.EMA(close_price)
        return pd.DataFrame({"Close": data.iloc[:,0], "EMA": ema})
    elif indicator == "Relative Strength index":
        close_float = [float(x) for x in data.iloc[:,0]]
        close_price = np.array(close_float)
        rsi = talib.RSI(close_price)
        return pd.DataFrame({"Close": data.iloc[:,0], "RSI": rsi})

st.title("Stock Data Analysis")
st.write("Simple app to download stock data and apply technical analysis indicators.")

st.sidebar.header("Stock Parameters")

available_tickers, tickers_companies_dict = get_ticker_components()

ticker = st.sidebar.selectbox(
    "Ticker", available_tickers, format_func=tickers_companies_dict.get
)

today = datetime.datetime.now()
last_year = datetime.date(today.year-1,today.month,today.day)

start = st.sidebar.date_input("Start date:", last_year, min_value=pd.Timestamp("1950-01-01"), max_value=today)
end = st.sidebar.date_input("End date:", today, min_value=pd.Timestamp("1950-01-01"))

data = yf.download(ticker, start, end)

selected_indicator = st.selectbox("Select a technical analysis indicator:", indicators)

indicator_data = apply_indicator(selected_indicator, data)

st.write(f"{selected_indicator} for {ticker}")
st.line_chart(indicator_data)

st.write("Stock data for", ticker)
st.dataframe(data)