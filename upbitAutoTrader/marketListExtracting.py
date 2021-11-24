# 종목정보 추출

import requests

url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

marketNameStr = eval(response.text)    # str to list -> list의 각 원소가 dict 총 267개
print(marketNameStr[0]['market'])      # list의 첫번째 원소가 dict형태니까 0번째 원소의 dict에서 'market'의 key값을 출력해준다.
print(len(marketNameStr))

# 모든 종목의 'market'의 key값을 새로운 list에 저장
marketName = []

for i in range(len(marketNameStr)):
    marketName.append(marketNameStr[i]['market'])

marketName_KRW = []
for i in marketName:                    # 각 원소에서 KRW가 아니면 전부다 제외 -> 근데 왜?? 남아있지..
    if i[:3] == 'KRW':                  # 새로운 list를 만들어서 'KRW'가 있는 문자열만 넣어주었더니 분류 완료
        marketName_KRW.append(i)

print(len(marketName_KRW))
# for i in marketName_KRW:
#     if 'MANA' in i:
#         print(marketName_KRW.index(i))