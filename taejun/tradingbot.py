import misc
import time
import telebot as tb


class TradingVB:
    def __init__(self, upbit, telegram, ratio, interval):
        self.upbit = upbit
        self.telegram = telegram
        self.ratio = ratio
        self.interval = interval
        self.state = "initial"
        self.next_state = "initial"
        self.base_hour = 9

    def set_upbit(self, upbit):
        self.upbit = upbit

    def set_telegram(self, telegram):
        self.telegram = telegram

    def set_state(self, state):
        self.state = state

    def set_next_state(self, next_state):
        self.next_state = next_state

    def set_ratio(self, ratio):
        self.ratio = ratio

    def set_interval(self, interval):
        self.interval = interval

    def set_base_hour(self, base_hour):
        self.base_hour = base_hour

    def run(self):
        _interval = misc.conv_interval(self.interval)
        base_min = self.base_hour * 60

        tickers_all = misc.get_tickers()
        tickers = misc.get_df_format()
        tickers = misc.set_tickers(tickers_all, tickers, ratio=self.ratio, interval=self.interval)

        bot = self.telegram

        while True:
            tm = misc.get_time()
            current_min = tm.tm_hour * 60 + tm.tm_min
            if base_min >= current_min:
                _min = (60 * 24) + current_min - base_min
            else:
                _min = current_min - base_min

            self.state = self.next_state

            if self.state == "stop":
                self.state = "stop"
                self.next_state = self.state
            elif _min % _interval == 0:
                self.state = "start"
                self.next_state = "running"
            elif self.state == "initial":
                self.state = "initial"
                self.next_state = self.state
            else:
                self.state = "running"
                self.next_state = self.state

            print("STATUS : ", self.state, end='')
            print(" / _min = %d, base_min = %d, current_min = %d, _interval = %d, ratio = %d" % (
                _min, base_min, current_min, _interval, self.ratio))

            if self.state == "start":
                print("[Update Tickers] ", end='')
                misc.print_time(tm)
                tickers = misc.set_tickers(tickers_all, tickers, ratio=self.ratio, interval=self.interval)
                self.state = "running"
                time.sleep(0.1)

            if self.state == "running":
                print("[Update Price] ", end='')
                misc.print_time(tm)
                misc.set_price(tickers)
                print(tickers)

                print("[Sell] ", end='')
                misc.print_time(tm)
                msg = misc.sell_order(self.upbit, tickers)
                tb.send_msg(bot=bot, msg=msg)

                print("[Buy] ", end='')
                misc.print_time(tm)
                msg = misc.buy_order(self.upbit, tickers)
                tb.send_msg(bot=bot, msg=msg)

            time.sleep(60)  # 1 minute
