import pyupbit

# 로그인
access = "kXXkgSrMYK5mlTPfKc4vmuBxxWxViQ0vJshxZD4G"          # 본인 값으로 변경
secret = "WYjYoDwNvjyFUbFjqfplo2DcAoht2jHTjxmWWYNz"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# 잔고조회
print(upbit.get_balance("KRW-DOGE"))     # KRW-DOGE 조회
print(upbit.get_balance("KRW-MED"))     # KRW-MED 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회