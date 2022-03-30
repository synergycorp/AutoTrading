import pyupbit
import misc
import tradingbot
import telebot as tb

K_RATIO = 0.5
INTERVAL = "minute240"  # minute3/5/10/15/30/60/240 and day


def main(ratio=K_RATIO, interval=INTERVAL):
    [access_key, secret_key] = misc.get_key()

    upbit = pyupbit.Upbit(access_key, secret_key)
    print("balance : %.0f" % misc.get_balance(upbit))

    # Telegram bot running
    bot = tb.set_bot(tb.get_token()[0])
    tb.run_telebot()

    # Strategy #1 - Volatility Breaks
    trading_vb = tradingbot.TradingVB(upbit, bot, ratio=K_RATIO, interval=INTERVAL)
    trading_vb.run()


if __name__ == "__main__":
    main()
