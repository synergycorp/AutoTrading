import pyupbit
import numpy as np
import pandas as pd


df = pyupbit.get_ohlcv("KRW-AXS", count = 10)          # 7일동안 KRW-BTC에 대한 get_ohlcv함수를 통해 값 들을 불러온다.
# 변동성 돌파 기준 범위 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

# range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)    # target의 첫번째 값은 이전날에 데이터가 없으니까 못구하니까 .shift(1)로 다음 칸에 결과값 작성

print(df)
# 전일대비 수익률 최고가(high) - 시작가(open) / 시작가(open) * 100
df['ascent rate'] = (df['high'] - df['open']) / df['open'] * 100

highAscentRate = df[df['ascent rate'] > 11]


print(highAscentRate)
print(len(highAscentRate))