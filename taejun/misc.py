import pyupbit
import os.path
import pandas as pd


def get_key():
    f = open(os.path.expanduser('~') + "/.upbit_key.dat", 'r')
    access_key = f.readline().split()[0]
    secret_key = f.readline().split()[0]

    return [access_key, secret_key]


def get_balance(upbit, ticker="KRW"):
    return upbit.get_balance(ticker)


def get_tickers(market="KRW"):
    # tickers_all = pyupbit.get_tickers(fiat='KRW')
    # tickers_krw = [i for i in tickers_all if i[:3] == "KRW"]
    tickers = pyupbit.get_tickers(market)
    return tickers


def sort_tickers(tickers, start=1, end=10, interval="minute240"):
    data = {
        'ticker': [],
        'volume': [],
        'volatility': [],
        'open': []
    }
    df = pd.DataFrame(data)
    for t in tickers:
        while True:
            temp = pyupbit.get_ohlcv(ticker=t, interval=interval, count=2)
            if temp is None:
                time.sleep(0.1)
                continue
            else:
                time.sleep(0.02)
                break
        new_data = [t,
                    temp['value'].values[0],
                    temp['high'].values[0] - temp['low'].values[0],
                    temp['open'].values[1]]
        df.loc[len(df)] = new_data
        sorted_df = df.sort_values(by=['volume'], ascending=False).reset_index(drop=True)

    return sorted_df[start - 1:end]


def get_price(ticker):
    return pyupbit.get_current_price(ticker=ticker)
