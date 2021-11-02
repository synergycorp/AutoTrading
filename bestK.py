import pyupbit
import numpy as np


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror      # 누적 수익률


for k in np.arange(0.1, 1.0, 0.1):  # k값을 0.1 부터 1.0까지 0.1씩 증가시킨다.
    ror = get_ror(k)                # 변화하는 k값에 따라 누적수익률을 구한다.
    print("%.1f %f" % (k, ror))