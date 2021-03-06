import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os.path


class TeleBot:
    def __init__(self):
        [t, d] = self.get_token()
        self.token = t
        self.chat_id = d
        self.bot = self.set_bot()
        self.query_data = "none"

    @staticmethod
    def get_token():
        f = open(os.path.expanduser('~') + "/.telegram_bot.dat", 'r')
        token = f.readline().split()[0]
        chat_id = int(f.readline().split()[0])

        return [token, chat_id]

    def set_bot(self):
        return telepot.Bot(self.token)

    def send_msg(self, msg):
        for m in msg:
            self.bot.sendMessage(self.chat_id, m)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if chat_id == self.chat_id:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='시작', callback_data='start'),
                 InlineKeyboardButton(text='멈춰', callback_data='stop')],
                [InlineKeyboardButton(text='간격변경', callback_data='set_interval'),
                 InlineKeyboardButton(text='예외설정', callback_data='set_exception')],
                [InlineKeyboardButton(text='보유종목', callback_data='show_balance'),
                 InlineKeyboardButton(text='기록보기', callback_data='show_log')],
                [InlineKeyboardButton(text='3분', callback_data='set_interval_3'),
                 InlineKeyboardButton(text='30분', callback_data='set_interval_30'),
                 InlineKeyboardButton(text='60분', callback_data='set_interval_60'),
                 InlineKeyboardButton(text='240분', callback_data='set_interval_240')],
                [InlineKeyboardButton(text='다팔아라', callback_data='sell_all')]
                 ])

            if msg['text'][0] == '/':
                self.bot.sendMessage(chat_id, '눌러', reply_markup=keyboard)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        self.query_data = query_data

        self.bot.answerCallbackQuery(query_id, text='알았다')

    def run_telebot(self):
        MessageLoop(self.bot, {'chat': self.on_chat_message,
                               'callback_query': self.on_callback_query}).run_as_thread()
        print('Listening ...')