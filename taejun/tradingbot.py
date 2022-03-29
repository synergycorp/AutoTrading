import misc
import time
import telebot as tb


def vb_bot(upbit, ratio=0.5, base_hour=9, interval="minute240"):
    # constraint : you can choose interval only in minute3/5/10/15/30/60/240 and day
    _interval = misc.conv_interval(interval)
    base_min = base_hour * 60

    tickers_all = misc.get_tickers()
    tickers = misc.get_df_format()
    tickers = misc.set_tickers(tickers_all, tickers, ratio=ratio, interval=interval)

    [bot, dt] = tb.get_token()
    state = "initial"

    while True:
        tm = misc.get_time()
        current_min = tm.tm_hour * 60 + tm.tm_min
        if base_min >= current_min:
            _min = (60 * 24) + current_min - base_min
        else:
            _min = current_min - base_min

        if _min % _interval == 0:
            state = "update"
        elif not state == "initial":
            state = "check"

        print("STATUS : ", state, end='')
        print(" / _min = %d, base_min = %d, current_min = %d, _interval = %d, ratio = %d" % (_min, base_min, current_min, _interval, ratio))

        if state == "update":
            print("[Update Tickers] ", end='')
            misc.print_time(tm)
            tickers = misc.set_tickers(tickers_all, tickers, ratio=ratio, interval=interval)

        if not state == "initial":
            print("[Update Price] ", end='')
            misc.print_time(tm)
            misc.set_price(tickers)
            print(tickers)

            print("[Sell] ", end='')
            misc.print_time(tm)
            msg = misc.sell_order(upbit, tickers)
            tb.send_msg(bot, dt, msg)

            print("[Buy] ", end='')
            misc.print_time(tm)
            msg = misc.buy_order(upbit, tickers)
            tb.send_msg(bot, dt, msg)

        time.sleep(60)  # 1 minute
