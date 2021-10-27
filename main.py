import yfinance as yf
import datetime

today = datetime.date.today()
start_date = today - datetime.timedelta(days=365)

crypto = ['BTC-USD', 'DOGE-USD', 'ETH-USD']


def yf_to_csv(crypto_lst, start_date, today):
    for i in crypto_lst:
        df = yf.download(i, start_date, today)
        df.to_csv("./datasets/" + i + ".csv")


yf_to_csv(crypto, start_date, today)
