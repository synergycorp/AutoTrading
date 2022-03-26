import pyupbit
import os.path
import time
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


def get_price(tickers):
    return pyupbit.get_current_price(ticker=tickers)


def set_tickers(tickers, ratio=0.5, start=1, end=10, interval="minute240"):
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

    trimmed_df = sorted_df[start - 1:end].copy()
    trimmed_df['target'] = trimmed_df['volatility'] * ratio + trimmed_df['open']

    return trimmed_df


def market_monitor(tickers):
    price = list(get_price(tickers['ticker']).values())
    buy_call = tickers.copy()
    buy_call['price'] = price
    buy_call['call'] = buy_call['price'] - buy_call['target'] >= 0
    buy_call = buy_call.drop(['volume', 'volatility', 'open', 'target', 'price'], axis=1)

    return buy_call


def get_time():
    tm = time.localtime()
    return tm


def print_time(tm):
    string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
    print(string)
    return string


def conv_interval(interval="minute240"):
    min_map = dict(minute1=3, minute3=3, minute5=5, minute10=10, minute15=15,
                   minute30=30, minute60=60, minute240=240, day=1440, week=1440)
    return min_map[interval]


def check_tickers(tickers):
    buy_call = market_monitor(tickers)
    buy_ticker = buy_call['ticker'].where(buy_call['call'] == True)
    buy_ticker = buy_ticker.dropna()
    if len(buy_ticker) == 0:
        print("---Negative")
    else:
        print("---[Woof Woof] : \"I found it\"")
        print(buy_ticker)  # Here needs to be some buy order
    return buy_ticker


def buy_tickers(tickers):
    return 0


def dump_tickers(tickers):
    return 0


def watchdog(ratio=0.5, base_hour=9, interval="minute240"):
    # constraint : you can choose interval only in minute3/5/10/15/30/60/240 and day
    _interval = conv_interval(interval)
    base_min = base_hour * 60

    tickers_all = get_tickers()
    tickers = set_tickers(tickers_all, ratio=ratio, interval=interval)

    setup_check = 0
    while True:  # When should I break it out ??
        tm = get_time()
        current_min = tm.tm_hour * 60 + tm.tm_min
        _min = base_min + current_min

        if _min % _interval == 0:
            print("[Volume Check] ", end='')
            print_time(tm)

            tickers = set_tickers(tickers_all, ratio=ratio, interval=interval)
            check_tickers(tickers)
            setup_check = 1

        if _min % _interval == _interval - 1:
            #   <-- need to check whether tickers are
            dump_tickers(tickers)
            print("[Dump It Out] ", end='')
            print_time(tm)

        else:
            #   <-- need to check whether tickers are
            check_tickers(tickers)
            print("[Volume Check] ", end='')
            print_time(tm)


        time.sleep(60)  # 1 minute
