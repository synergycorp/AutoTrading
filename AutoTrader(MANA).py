import time
import pyupbit
import datetime

access = "TlKLmK7jp8apGBVlKLbYyrQJjpJJsK2MJc1ZSNSC"
secret = "AefE6iuSNwdyEvP5a85d2B4TkO3Fhbx0iXpCLapw"

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

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma15

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
        now = datetime.datetime.now()                                   # 현재시간
        start_time = get_start_time("KRW-MANA")                         # 투자시작시간
        end_time = start_time + datetime.timedelta(days=1)              # 투자종료시간

        # 9:00 < 현재 < 8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-MANA", 0.5)             # 목표가 설정
            ma5 = get_ma5("KRW-MANA")
            current_price = get_current_price("KRW-MANA")                # 현재가 확인
            if target_price < current_price and ma5 < current_price:                            # 목표가보다 현재가가 높으면
                krw = get_balance("KRW")                                # 내 잔고를 조회하고
                if krw > 5000:                                          # 잔고가 5000원 이상이면
                    upbit.buy_market_order("KRW-MANA", krw*0.9995)       # 코인매수 인자값으로 비트코인값과, 잔고 * 수수로 0.05%
        else:
            mana = get_balance("MANA")                                    # 현재 mana잔고 체크
            if mana > 5000:                                           # 0.00008mana이상이면 전량 매도
                upbit.sell_market_order("KRW-MANA", mana*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)