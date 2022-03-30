import pyupbit
import misc
import tradingbot

K_RATIO = 0.5
INTERVAL = "minute240"  # minute3/5/10/15/30/60/240 and day


def main(ratio=K_RATIO, interval=INTERVAL):
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))

    # Strategy #1 - Volatility Breaks
    tradingbot.vb_bot(upbit, ratio=ratio, interval=interval)


if __name__ == "__main__":
    main()
