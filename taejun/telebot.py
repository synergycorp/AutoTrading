import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os.path
import time


def get_token():
    f = open(os.path.expanduser('~') + "/.telegram_bot.dat", 'r')
    token = f.readline().split()[0]
    target_id = int(f.readline().split()[0])

    return [token, target_id]


[t, d] = get_token()
bot = telepot.Bot(t)


def set_bot(token):
    _bot = telepot.Bot(token)
    return _bot


def send_msg(_bot, dt, msg):
    print(type(_bot))
    for m in msg:
        _bot.sendMessage(dt, m)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if chat_id == d:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='시작', callback_data='start'),
             InlineKeyboardButton(text='멈춰', callback_data='stop')],
            [InlineKeyboardButton(text='간격변경', callback_data='set_interval'),
             InlineKeyboardButton(text='예외설정', callback_data='set_exception')],
            [InlineKeyboardButton(text='보유종목', callback_data='show_balance'),
             InlineKeyboardButton(text='기록보기', callback_data='show_log')],
        ])

        bot.sendMessage(chat_id, '눌러', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='알았다')


def run_telebot():
    MessageLoop(bot, {'chat': on_chat_message,
                      'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')

    while 1:
        time.sleep(1)
