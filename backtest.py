import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume, value)로 시가, 고가, 저가, 종가, 거래량, 거래대금에 대한 데이터
# def get_ohlcv(ticker="KRW-BTC", interval="day", count=200, to=None, period=0.1):
# 날짜 값 인자 "%Y-%m-%d %H:%M:%S"
df = pyupbit.get_ohlcv("KRW-MANA", count = 31, to = '2021-08-31 09:00:00')          # 7일동안 KRW-BTC에 대한 get_ohlcv함수를 통해 값 들을 불러온다.

# 변동성 돌파 기준 범위 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

# range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)    # target의 첫번째 값은 이전날에 데이터가 없으니까 못구하니까 .shift(1)로 다음 칸에 결과값 작성

# np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.round_(np.where(df['high'] > df['target'], df['close'] / df['target'], 1), 4)
# 누적 곱 계산(cumprod) => 누적 수익률, cumprod() 각 원소들의 누적 곱
df['hpr'] = np.round_(df['ror'].cumprod(), 4)

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['dd'].max())

# excel로 출력
df.to_excel("C:/coding/Python/AutoTrading/backtest/MANA(210801 ~ 210831).xlsx")