import pyupbit

# 로그인
access = "TlKLmK7jp8apGBVlKLbYyrQJjpJJsK2MJc1ZSNSC"          # 본인 값으로 변경
secret = "AefE6iuSNwdyEvP5a85d2B4TkO3Fhbx0iXpCLapw"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# 잔고조회
print(upbit.get_balance("KRW-MANA"))     # KRW-DOGE 조회
print(upbit.get_balance("KRW-MED"))     # KRW-MED 조회 예약 매도, 매수가 걸려있으면 안된다.
print(upbit.get_balance("MED"))     # KRW-MED 조회 예약 매도, 매수가 걸려있으면 안된다.
print(upbit.get_balance("KRW"))         # 보유 현금 조회