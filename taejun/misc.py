import pyupbit
import os.path
import time
import pandas as pd

EXCEPTION = ['KRW-MLK', 'KRW-BTT']


def get_key():
    f = open(os.path.expanduser('~') + "/.upbit_key.dat", 'r')
    access_key = f.readline().split()[0]
    secret_key = f.readline().split()[0]

    return [access_key, secret_key]


def get_balance(upbit, ticker="KRW"):
    return upbit.get_balance(ticker)


def get_tickers(market="KRW"):
    tickers = pyupbit.get_tickers(market)
    return tickers


def get_price(tickers):
    return pyupbit.get_current_price(ticker=tickers)


def get_df_format():
    data = {
        'ticker': [],  # will be index
        'buy_target': [],
        'price': [],
        'stoploss_target': [],
        'volume': [],
        'open': [],
        'unit': [],
        'done': []
    }

    df = pd.DataFrame(data).set_index('ticker', drop=True)
    df['done'] = df['done'].astype(bool)

    return df


def set_price(tickers):
    tickers['price'] = list(get_price(tickers.index).values())


def set_tickers(tickers_all, tickers, ratio=0.5, start=1, end=10, interval="minute240"):
    df0 = get_df_format()

    for t in tickers.index:  # holdings processing
        if t in EXCEPTION:
            continue
        if not tickers.loc[[t], ['done']].values:
            continue
        while True:
            temp = pyupbit.get_ohlcv(ticker=t, interval=interval, count=2)
            if temp is None:
                time.sleep(0.1)
                continue
            else:
                time.sleep(0.02)
                break
        stoploss_0 = temp['open'].values[1] * 0.98
        stoploss_1 = tickers.loc[[t], ['buy_target']].values * 0.98
        tickers.loc[[t], ['stoploss_target']] = max(stoploss_0, stoploss_1)
        tickers.loc[[t], ['open']] = temp['open'].values[1]
        df0 = pd.concat([df0, tickers.loc[[t]]])

    numof_holdings = len(df0)

    df1 = get_df_format()

    for t in tickers_all:
        if t in EXCEPTION:
            continue
        if t in df0.index:  # pass holdings
            continue
        while True:
            temp = pyupbit.get_ohlcv(ticker=t, interval=interval, count=2)
            if temp is None:
                time.sleep(0.1)
                continue
            else:
                time.sleep(0.02)
                break
        new_data = {
            'ticker': [t],  # will be index
            'buy_target': [(temp['high'].values[0] - temp['low'].values[0]) * ratio + temp['open'].values[1]],
            'price': [0],
            'stoploss_target': [0],
            'volume': [temp['value'].values[0]],
            'open': [temp['open'].values[1]],
            'unit': [0]
            'done': [False]
        }
        new_df = pd.DataFrame(new_data).set_index('ticker', drop=True)
        df1 = pd.concat([df1, new_df])

    sorted_df = df1.sort_values(by=['volume'], ascending=False)

    trimmed_df = sorted_df[start - 1:end - numof_holdings].copy()
    merged_df = pd.concat([df0, trimmed_df])

    return merged_df


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
    unit = int((get_balance(upbit) / sum(tickers.done == False)) / 1000) * 1000 * 2
    # unit = 10000
    print("unit : %d" % unit)
    msg = []
    for t in tickers.index:
        cond_0 = tickers.loc[[t], ['done']].values == False
        cond_1 = tickers.loc[[t], ['price']].values >= tickers.loc[[t], ['buy_target']].values
        cond = cond_0 & cond_1
        if cond:
            upbit.buy_market_order(t, unit)
            tickers.loc[[t], ['done']] = True
            tickers.loc[[t], ['unit']] = unit
            msg.append("[매수] %s → %.1f (총 %d 원)" % (t[4:], tickers.loc[[t], ['price']].values, unit))
            print(msg[len(msg) - 1])
            time.sleep(0.1)
    return msg


def sell_order(upbit, tickers):
    msg = []
    for t in [t for t in tickers.index if tickers.loc[[t], ['done']].values]:
        if tickers.loc[[t], ['price']].values < tickers.loc[[t], ['stoploss_target']].values:
            amount = get_balance(upbit, t[4:])  # drop KRW-
            upbit.sell_market_order(t, amount)
            msg.append("[매도] %s → %.1f (총 %d 원)" % (t[4:], tickers.loc[[t], ['price']].values, tickers.loc[[t], ['unit']].values))
            print(msg[len(msg) - 1])
            time.sleep(0.1)
    return msg
