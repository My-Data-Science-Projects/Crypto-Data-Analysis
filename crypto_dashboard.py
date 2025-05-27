import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("""
# Cryptocurrency Dashboard Application
**Visually Show Data on Crypto (BTC, DOGE & ETH)**
""")

try:
    icon_image = Image.open('Ethereum-Bitcoin-Dogecoin.jpg')
    st.sidebar.image(icon_image, use_container_width=True)
except Exception as e:
    st.sidebar.write("Icon image not found or could not be loaded.")

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

# def get_data(symbol, start, end):
#     end_dt = datetime.date.today()
#     start_dt = start
#     symbol = symbol.upper()
#     if symbol == "BTC":
#         df = yf.download('BTC-USD', start_dt, end_dt)
#     elif symbol == "ETH":
#         df = yf.download('ETH-USD', start_dt, end_dt)
#     elif symbol == "DOGE":
#         df = yf.download('DOGE-USD', start_dt, end_dt)
#     else:
#         df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])

#     if isinstance(df.columns, pd.MultiIndex):
#         df.columns = df.columns.get_level_values(0)

#     start = pd.to_datetime(start)
#     end = pd.to_datetime(end)

#     return df.loc[start:end]

def get_data(symbol, start, end):
    end_dt = datetime.date.today()
    start_dt = start
    symbol = symbol.upper()
    if symbol == "BTC":
        df = yf.download('BTC-USD', start_dt, end_dt)
    elif symbol == "ETH":
        df = yf.download('ETH-USD', start_dt, end_dt)
    elif symbol == "DOGE":
        df = yf.download('DOGE-USD', start_dt, end_dt)
    else:
        df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Filter only the needed columns and reorder
    columns_needed = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df.loc[:, columns_needed]

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

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
    )]
)

st.header(f"{crypto_name} Data")
st.write(df)

st.header(f"{crypto_name} Data Statistics")
st.write(df.describe())

st.header(f"{crypto_name} Close Price")
st.line_chart(df['Close'])

st.header(f"{crypto_name} Volume")
st.bar_chart(df['Volume'])

st.header(f"{crypto_name} Candle Stick")
st.plotly_chart(fig)
