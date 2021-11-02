import time
import pyupbit
import datetime

access = "your-access"
secret = "your-secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        # 9:00 < 현재 < 8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)             # 목표가 설정
            current_price = get_current_price("KRW-BTC")                # 현재가 확인
            if target_price < current_price:                            # 목표가보다 현재가가 높으면
                krw = get_balance("KRW")                                # 내 잔고를 조회하고
                if krw > 5000:                                          # 잔고가 5000원 이상이면
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)       # 코인매수 인자값으로 비트코인값과, 잔고 * 수수로 0.05%
        else:
            btc = get_balance("BTC")                                    # 현재 btc잔고 체크
            if btc > 0.00008:                                           # 0.00008btc이상이면 전량 매도
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)