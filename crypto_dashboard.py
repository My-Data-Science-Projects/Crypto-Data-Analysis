# Description: Build a Cryptocurrency Dashboard

# Import Libraries
import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image

st.write("""
# Cryptocurrency Dashboard Application
** Visually Show Data on Crypto (BTC, DOGE & ETH) **
""")

#image = Image.open('Ethereum-Bitcoin-Dogecoin.jpg')
#st.image(image, use_column_width=True)

st.sidebar.header("User Input")


def get_input():
    to_date = datetime.date.today()
    from_date = to_date - datetime.timedelta(days=15)
    start_date = st.sidebar.date_input('Start Date', from_date)
    end_date = st.sidebar.date_input('End Date', to_date)
    coins = ['BTC', 'ETH', 'DOGE']
    crypto_symbol = st.sidebar.selectbox('Select Crypto Symbol', coins)
    return start_date, end_date, crypto_symbol


def get_crypto_name(symbol):
    symbol = symbol.upper()
    if symbol == "BTC":
        return "Bitcoin"
    if symbol == "ETH":
        return "Ethereum"
    if symbol == "DOGE":
        return "Dogecoin"
    else:
        return "None"


def get_data(symbol, start, end):
    end_dt = datetime.date.today()
    # start_dt = end_dt - datetime.timedelta(days=365)
    start_dt = start
    symbol = symbol.upper()
    if symbol == "BTC":
        # df = pd.read_csv("C:/Users/akash/Desktop/crypto dashboard/datasets/BTC-USD.csv")
        df = yf.download('BTC-USD', start_dt, end_dt)
    elif symbol == "ETH":
        # df = pd.read_csv("C:/Users/akash/Desktop/crypto dashboard/datasets/ETH-USD.csv")
        df = yf.download('ETH-USD', start_dt, end_dt)
    elif symbol == "DOGE":
        # df = pd.read_csv("C:/Users/akash/Desktop/crypto dashboard/datasets/DOGE-USD.csv")
        df = yf.download('DOGE-USD', start_dt, end_dt)
    else:
        df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # df = df.set_index(df['Date'].values)

    return df.loc[start:end]


start, end, symbol = get_input()
df = get_data(symbol, start, end)
crypto_name = get_crypto_name(symbol)

fig = go.Figure(
    data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
    )
    ]
)

st.header(crypto_name + " Data")
st.write(df)

st.header(crypto_name + " Data Statistics")
st.write(df.describe())

st.header(crypto_name + " Close Price")
st.line_chart(df['Close'])

st.header(crypto_name + " Volume")
st.bar_chart(df['Volume'])

st.header(crypto_name + " Candle Stick")
st.plotly_chart(fig)
