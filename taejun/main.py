import pyupbit
import misc

K_RATIO = 0.05
INTERVAL = "minute3"  # minute3/5/10/15/30/60/240 and day


def main(ratio=K_RATIO, interval=INTERVAL):
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))

    # tickers_all = misc.get_tickers()
    # print("tickers : %s" % tickers_all)
    # tickers = misc.set_tickers(tickers_all, ratio=K_RATIO)
    # print("%s" % tickers)
    # print("price : %s" % misc.get_price(tickers['ticker']))
    # print("buy_call : \n%s" % misc.market_monitor(tickers))

    misc.watchdog(upbit, ratio=ratio, interval=interval)


if __name__ == "__main__":
    main()
