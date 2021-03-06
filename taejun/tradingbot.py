import misc
import time
import pandas as pd


class TradingVB:
    def __init__(self, upbit, telegram, ratio, interval):
        self.upbit = upbit
        self.telegram = telegram
        self.ratio = ratio
        self.interval = interval
        self.state = "initial"
        self.next_state = "initial"
        self.base_hour = 9
        self.tickers = misc.get_df_format()

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

    def set_tickers(self, tickers_all):
        self.tickers = misc.set_tickers(tickers_all=tickers_all, tickers=self.tickers,
                                        ratio=self.ratio, interval=self.interval)

    def get_holdings(self):
        return self.tickers.loc[self.tickers['done'] & (self.tickers['sell_done'] == False)]

    def sell_all(self):
        holdings = self.get_holdings()
        if len(holdings) == 0:
            self.telegram.send_msg(["보유종목이 없습니다."])
            return
        else:
            print("test4")
            msg = misc.sell_order(self.upbit, holdings)
            print("test5")
            for t in holdings.index:
                print("testtest", t)
                self.tickers.loc[[t], ['sell_done']] = True
            self.telegram.send_msg(msg=msg)

    def run(self):
        _interval = misc.conv_interval(self.interval)
        base_min = self.base_hour * 60

        tickers_all = misc.get_tickers()
        # tickers = misc.get_df_format()
        # tickers = misc.set_tickers(tickers_all, tickers, ratio=self.ratio, interval=self.interval)
        self.set_tickers(tickers_all)

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
                # tickers = misc.set_tickers(tickers_all, tickers, ratio=self.ratio, interval=self.interval)
                self.set_tickers(tickers_all)
                self.state = "running"
                time.sleep(0.1)

            if self.state == "running":
                print("[Update Price] ", end='')
                misc.print_time(tm)
                misc.set_price(self.tickers)
                print(self.tickers)

                print("[Sell] ", end='')
                misc.print_time(tm)
                msg = misc.sell_order(self.upbit, self.tickers)
                self.telegram.send_msg(msg=msg)

                print("[Buy] ", end='')
                misc.print_time(tm)
                msg = misc.buy_order(self.upbit, self.tickers)
                self.telegram.send_msg(msg=msg)

            # How can I make it interrupt : reference each other
            if self.telegram.query_data in ["start"]:
                self.telegram.send_msg(["시작합니다."])
                self.next_state = self.telegram.query_data
            elif self.telegram.query_data in ["stop"]:
                self.telegram.send_msg(["종료합니다."])
                self.next_state = self.telegram.query_data
            elif self.telegram.query_data == "set_interval":
                self.telegram.send_msg(["개발중입니다."])
            elif self.telegram.query_data == "set_exception":
                self.telegram.send_msg(["개발중입니다."])
            elif self.telegram.query_data == "show_balance":
                self.telegram.send_msg([t[4:] for t in self.tickers.index if self.tickers.loc[[t], ['done']].values])
                # self.telegram.send_msg([t[4:] for t in self.get_holdings.index])
            elif self.telegram.query_data == "show_log":
                self.telegram.send_msg(["개발중입니다."])
            elif self.telegram.query_data[:13] == "set_interval_":
                print(self.telegram.query_data[13:])
                self.telegram.send_msg(["간격을 %s분으로 바꿉니다." % self.telegram.query_data[13:]])
                self.set_interval(self.telegram.query_data[13:])
            elif self.telegram.query_data == "sell_all":
                self.telegram.send_msg(["다 팔라고 하셨습니다."])
                self.sell_all()
            self.telegram.query_data = "none"

            time.sleep(1)  # Issue : Interrupt during Infinite loop
