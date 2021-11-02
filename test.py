import pyupbit

# 로그인
access = "7e7ZjqwdEJ5HxlJoWDVunZJRh3m7i7r6v6Ro7SZW"          # 본인 값으로 변경
secret = "tJBoSNiNmjYlxMbBiCKAEzds6DtUufIEXreMVaCF"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# 잔고조회
print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW-MED"))     # KRW-MED 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회