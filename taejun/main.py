import pyupbit
import misc


def main():
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))
    print("tickers : %s" % misc.get_tickers())
    abc = misc.get_tickers()
    print("top tickers : %s" % misc.sort_tickers(abc))


if __name__ == "__main__":
    main()
