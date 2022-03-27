import pyupbit
import os.path
import time
import pandas as pd

EXCEPTION = ['KRW-MLK']


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


def set_tickers(tickers, ratio=0.5, start=1, end=20, interval="minute240"):
    data = {
        'ticker': [],       # will be index
        'target': [],
        'price': [],
        'volume': [],
        'volatility': [],
        'open': [],
        'call': [],
        'done': []
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
                    0,
                    0,
                    temp['value'].values[0],
                    temp['high'].values[0] - temp['low'].values[0],
                    temp['open'].values[1],
                    False,
                    False]
        df.loc[len(df)] = new_data
        sorted_df = df.sort_values(by=['volume'], ascending=False).reset_index(drop=True)

    trimmed_df = sorted_df[start - 1:end].copy()
    trimmed_df['target'] = trimmed_df['volatility'] * ratio + trimmed_df['open']
    trimmed_df = trimmed_df.set_index('ticker', drop=True)

    return trimmed_df


def market_monitor(tickers):
    price = list(get_price(tickers.index).values())

    tickers['price'] = price
    tickers['call'] = tickers['price'] - tickers['target'] >= 0

    return tickers


def get_time():
    tm = time.localtime()
    return tm


def print_time(tm):
    string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
    print(string)
    return string


def conv_interval(interval="minute240"):
    min_map = dict(minute1=2, minute3=3, minute5=5, minute10=10, minute15=15,
                   minute30=30, minute60=60, minute240=240, day=1440, week=1440, month=1440)
    return min_map[interval]


def buy_order(upbit, tickers):
    market_monitor(tickers)
    print(tickers)
    unit = int((get_balance(upbit) / sum(tickers.done==False))/1000)*1000*2
    print("unit : %d" % unit)
    for t in tickers.index:
        if t in EXCEPTION: continue
        elif tickers.loc[[t], ['call']].values & (not tickers.loc[[t], ['done']].values):
            upbit.buy_market_order(t, unit)
            tickers.loc[[t], ['done']] = True
            print(t, "is bought.")
            time.sleep(0.1)
    return 0


def dump_order(upbit, tickers):
    for t in tickers.index:
        if tickers.loc[[t], ['done']].values:
            print(t[4:])
            amount = get_balance(upbit, t[4:])
            upbit.sell_market_order(t, amount)
            print(t, "is sold.")
            time.sleep(0.1)
    return 0


def watchdog(upbit, ratio=0.5, base_hour=9, interval="minute240"):
    # constraint : you can choose interval only in minute3/5/10/15/30/60/240 and day
    _interval = conv_interval(interval)
    base_min = base_hour * 60

    tickers_all = get_tickers()
    tickers = set_tickers(tickers_all, ratio=ratio, interval=interval)

    while True:
        tm = get_time()
        current_min = tm.tm_hour * 60 + tm.tm_min
        if base_min >= current_min:
            _min = (60*24) + current_min - base_min
        else:
            _min = current_min - base_min
        print("_min = %d, base_min = %d, current_min = %d, _interval = %d" % (_min, base_min, current_min, _interval))

        # this is because time lagging
        if _min % _interval == 0:
            state = "update"
        elif _min % _interval == _interval - 1:
            state = "close"
        else:
            state = "check"

        if state == "update":
            print("[Update] ", end='')
            print_time(tm)
            tickers = set_tickers(tickers_all, ratio=ratio, interval=interval)

            print("[Buy0] ", end='')
            print_time(tm)
            buy_order(upbit, tickers)

        elif state == "close":
            dump_order(upbit, tickers)
            print("[Dump] ", end='')
            print_time(tm)

        elif state == "check":
            print("[Buy1] ", end='')
            print_time(tm)
            buy_order(upbit, tickers)

        time.sleep(60)  # 1 minute
