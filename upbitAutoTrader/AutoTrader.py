import time
import pyupbit
import datetime
import numpy as np
import pandas as pd
import requests

access = "TlKLmK7jp8apGBVlKLbYyrQJjpJJsK2MJc1ZSNSC"
secret = "AefE6iuSNwdyEvP5a85d2B4TkO3Fhbx0iXpCLapw"

# 종목정보 추출
url = "https://api.upbit.com/v1/market/all?isDetails=false"
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers)
marketNameStr = eval(response.text)    # str to list -> list의 각 원소가 dict 총 267개

# 원화 마켓에 있는 종목 정보들을 list형태로 저장
def marketListExtracting(marketNameStr):
    marketName = []                         # 모든 종목의 'market'의 key값을 새로운 list에 저장           
    for i in range(len(marketNameStr)):
        marketName.append(marketNameStr[i]['market'])

    marketName_KRW = []
    for i in marketName:                    # 각 원소에서 KRW가 아니면 전부다 제외 -> 근데 왜?? 남아있지..
        if i[:3] == 'KRW':                  # 새로운 list를 만들어서 'KRW'가 있는 문자열만 넣어주었더니 분류 완료
            marketName_KRW.append(i)
    return marketName_KRW

# 조건에 맞는 종목들을 list에 저장
def investmentListExtracing(marketName_KRW):
    investmentList = []
    timeBreaker = 0
    for i in marketName_KRW:                                # KRW market에 있는 종목 반복
        df = pyupbit.get_ohlcv(i, count = 30)               # 7일동안 KRW-BTC에 대한 get_ohlcv함수를 통해 값 들을 불러온다.

        df['ascent rate'] = (df['high'] - df['open']) / df['open'] * 100    # 당일 시작가와 최고가를 통해 수익률 column추가

        highAscentRate = df[df['ascent rate'] > 11]         # boolean type에서 df type으로 변경, 종목에서 'ascent rate' 비율이 11%가 증가하는 날짜

        print(i, len(highAscentRate), sep=':')              # 종목 정보와 30일동안 수익률이 11%가 넘는 날짜의 수
        if len(highAscentRate) > 10:                        # 30일 동안 수익률이 11%가 넘는 날짜의 수가 11일 이상이면 투자리스트에 추가
            investmentList.append(i)
        
        timeBreaker += 1
        if timeBreaker % 10 == 0:
            time.sleep(1)
    return investmentList

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
    return ma5

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
investmentList = investmentListExtracing(marketListExtracting(marketNameStr))   # 투자 리스트 추출
print("autotrade start")

# 자동매매 시작
while True:
    try:
        for i in investmentList:                                    # 투자리스에 있는 종목을
            now = datetime.datetime.now()                           # 현재시간
            start_time = get_start_time(i)                          # 투자시작시간
            end_time = start_time + datetime.timedelta(days=1)      # 투자종료시간

            # 9:00 < 현재 < 8:59:50
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(i, 0.5)             # 목표가 설정
                current_price = get_current_price(i)                # 현재가 확인
                if target_price < current_price:                    # 목표가보다 현재가가 높으면
                    krw = get_balance("KRW")                        # 내 잔고를 조회하고
                    if krw > 5000:                                  # 잔고가 5000원 이상이면
                        upbit.buy_market_order(i, krw*0.9995)       # 코인매수 인자값으로 종목과, 잔고 * 수수로 0.05%
                        purchase_price = get_balance(i)

                    if current_price > purchase_price * 1.1:        # 현재 가격이 주문가격보다 10% 보다 크면 전량매도
                        upbit.sell_market_order(i, get_balance(i)*0.9995)                  # 현재 가격에 수수료를 곱하고 전량 매도
            
            # 8:59:50 ~ 9:00 시간이면
            else:
                currentCoinBalance = get_balance(i)                                    # 현재 종목잔고 체크
                upbit.sell_market_order(i, currentCoinBalance*0.9995)                  # 현재 가격에 수수료를 곱하고 전량 매도
            time.sleep(1)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)