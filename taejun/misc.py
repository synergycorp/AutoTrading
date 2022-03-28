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
        'call': [],
        'done': []
    }

    df = pd.DataFrame(data).set_index('ticker', drop=True)
    df['call'] = df['call'].astype(bool)
    df['done'] = df['done'].astype(bool)

    return df


def set_price(tickers):
    tickers['price'] = list(get_price(tickers.index).values())
    return 0


def set_tickers(tickers_all, tickers, ratio=0.5, start=1, end=10, interval="minute240"):
    df = get_df_format()

    for t in tickers.index:       # holdings processing
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
        t['stoploss_target'] = temp['open'].values[1] * 0.99
        t['open'] = temp['open'].values[1]
        df = pd.concat([df, t])

    numof_holdings = len(df)

    for t in tickers_all:
        if t in EXCEPTION:
            continue
        if t in df:     # pass holdings
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
            'call': [False],
            'done': [False]
        }
        new_df = pd.DataFrame(new_data).set_index('ticker', drop=True)
        # print(df, "test999")
        df = pd.concat([df, new_df])

    sorted_df = df.sort_values(by=['volume'], ascending=False)

    trimmed_df = sorted_df[start - 1:end - numof_holdings].copy()
    set_price(trimmed_df)

    return trimmed_df


def set_buy_target(tickers):
    tickers['call'] = tickers['price'] - tickers['buy_target'] >= 0

    return 0


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
    # unit = int((get_balance(upbit) / sum(tickers.done == False)) / 1000) * 1000 * 2
    unit = 10000
    print("unit : %d" % unit)
    for t in tickers.index:
        if tickers.loc[[t], ['call']].values & (not tickers.loc[[t], ['done']].values):
            upbit.buy_market_order(t, unit)
            tickers.loc[[t], ['done']] = True
            print(t, "is bought for %.1f" % tickers.loc[[t], ['price']].values)
            time.sleep(0.1)
    return 0


def sell_order(upbit, tickers):
    for t in [t for t in tickers.index if tickers.loc[[t], ['done']].values]:
        if tickers.loc[[t], ['price']].values < tickers.loc[[t], ['stoploss_target']].values:
            amount = get_balance(upbit, t[4:])  # drop KRW-
            upbit.sell_market_order(t, amount)
            print(t, "is sold for %.1f" % tickers.loc[[t], ['price']].values)
            time.sleep(0.1)
    return 0


def watchdog(upbit, ratio=0.5, base_hour=9, interval="minute240"):
    # constraint : you can choose interval only in minute3/5/10/15/30/60/240 and day
    _interval = conv_interval(interval)
    base_min = base_hour * 60

    tickers_all = get_tickers()
    tickers = get_df_format()
    tickers = set_tickers(tickers_all, tickers, ratio=ratio, interval=interval)

    state = "initial"

    while True:
        tm = get_time()
        current_min = tm.tm_hour * 60 + tm.tm_min
        if base_min >= current_min:
            _min = (60 * 24) + current_min - base_min
        else:
            _min = current_min - base_min

        if _min % _interval == 0:
            state = "update"
        elif not state == "initial":
            state = "check"

        print("STATUS : ", state, end='')
        print(" / _min = %d, base_min = %d, current_min = %d, _interval = %d, ratio = %d" % (_min, base_min, current_min, _interval, ratio))

        if state == "update":
            print("[Update] ", end='')
            print_time(tm)
            tickers = set_tickers(tickers_all, tickers, ratio=ratio, interval=interval)
            print(tickers)

            print("[Sell0] ", end='')
            print_time(tm)
            sell_order(upbit, tickers)

            print("[Buy0] ", end='')
            print_time(tm)
            set_buy_target(tickers)
            buy_order(upbit, tickers)

        elif state == "check":
            print("[Get Price] ", end='')
            print_time(tm)
            set_price(tickers)
            print(tickers)

            print("[Sell1] ", end='')
            print_time(tm)
            sell_order(upbit, tickers)

            print("[Buy1] ", end='')
            print_time(tm)
            set_buy_target(tickers)
            buy_order(upbit, tickers)

        time.sleep(60)  # 1 minute