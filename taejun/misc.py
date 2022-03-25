import pyupbit
import os.path
import time
import numpy as np


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
    tickers_vol = []
    for t in tickers:
        while True:
            temp = pyupbit.get_ohlcv(ticker=t, interval=interval, count=2)
            if temp is None:
                time.sleep(0.1)
                continue
            else:
                time.sleep(0.02)
                break
        volumes = [t, temp['high'].values[0] - temp['low'].values[0], temp['value'].values[0]]
        tickers_vol.append(volumes)

    tickers_vol.sort(key=lambda x: x[2], reverse=True)  # descending order
    tickers_vol = np.array(tickers_vol)
    np.delete(tickers_vol, 2, axis=1)

    return tickers_vol[start - 1:end]