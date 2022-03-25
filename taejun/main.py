import pyupbit
import misc

K_RATIO = 0.5

def main():
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))
    tickers_all = misc.get_tickers()
    print("tickers : %s" % tickers_all)
    tickers = misc.set_tickers(tickers_all, ratio=K_RATIO)
    print("%s" % tickers)
    # print("prices : %s" % misc.get_price(tickers['ticker'].values))
    print("price : %s" % misc.get_price(tickers['ticker']))
    # print("XRP price : %s" % misc.get_price(tickers['ticker'])['KRW-XRP'])
    # print("price2 : %s" % list(misc.get_price(tickers['ticker']).values()))
    print("buy_call : \n%s" % misc.market_monitor(tickers))


if __name__ == "__main__":
    main()
