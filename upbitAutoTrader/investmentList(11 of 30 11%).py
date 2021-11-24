import pyupbit
import numpy as np
import pandas as pd
import requests
import time

# 종목정보 추출

url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

marketNameStr = eval(response.text)    # str to list -> list의 각 원소가 dict 총 267개

def marketListExtracting(marketNameStr):
    marketName = []                         # 모든 종목의 'market'의 key값을 새로운 list에 저장           
    for i in range(len(marketNameStr)):
        marketName.append(marketNameStr[i]['market'])

    marketName_KRW = []
    for i in marketName:                    # 각 원소에서 KRW가 아니면 전부다 제외 -> 근데 왜?? 남아있지..
        if i[:3] == 'KRW':                  # 새로운 list를 만들어서 'KRW'가 있는 문자열만 넣어주었더니 분류 완료
            marketName_KRW.append(i)
    return marketName_KRW

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

result = investmentListExtracing(marketListExtracting(marketNameStr))
print(result)
#print(investmentListExtracing(marketName_KRW))

# investmentList = []
# timeBreaker = 0
# i = "KRW-MANA"
# #for i in marketName_KRW:                                # KRW market에 있는 종목 반복
# df = pyupbit.get_ohlcv(i, count = 30)               # 7일동안 KRW-BTC에 대한 get_ohlcv함수를 통해 값 들을 불러온다.

# df['range'] = (df['high'] - df['low']) * 0.5
# df['target'] = df['open'] + df['range'].shift(1)    # target의 첫번째 값은 이전날에 데이터가 없으니까 못구하니까 .shift(1)로 다음 칸에 결과값 작성
# df['ascent rate'] = (df['high'] - df['open']) / df['open'] * 100    # 당일 시작가와 최고가를 통해 수익률 column추가

# highAscentRate = df[df['ascent rate'] > 11]         # boolean type에서 df type으로 변경, 종목에서 'ascent rate' 비율이 11%가 증가하는 날짜

# print(df)
# print(i, len(highAscentRate), sep=':')              # 종목 정보와 30일동안 수익률이 11%가 넘는 날짜의 수
# if len(highAscentRate) > 10:                        # 30일 동안 수익률이 11%가 넘는 날짜의 수가 11일 이상이면 투자리스트에 추가
#     investmentList.append(i)

# timeBreaker += 1
# if timeBreaker % 10 == 0:
#     time.sleep(1)

# print(investmentList)