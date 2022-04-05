import pyupbit
import misc
import tradingbot
import telebot
from threading import Thread

K_RATIO = 0.4
INTERVAL = "minute240"  # minute3/5/10/15/30/60/240 and day


def main(ratio=K_RATIO, interval=INTERVAL):
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))

    tb = telebot.TeleBot()
    trading_vb = tradingbot.TradingVB(upbit, tb, ratio=K_RATIO, interval=INTERVAL)

    # Telegram bot running
    th1 = Thread(target=tb.run_telebot())
    th1.start()

    # Strategy #1 - Volatility Breaks
    th2 = Thread(trading_vb.run())
    th2.start()

    th1.join()
    th2.join()


if __name__ == "__main__":
    main()
