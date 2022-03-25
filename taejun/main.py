import pyupbit
import misc


def main():
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))
    tickers_all = misc.get_tickers()
    print("tickers : %s" % tickers_all)
    tickers = misc.sort_tickers(tickers_all)
    print("%s" % tickers)
    # print("prices : %s" % misc.get_price(tickers))


if __name__ == "__main__":
    main()
