import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os.path
import time


def get_token():
    f = open(os.path.expanduser('~') + "/.telegram_bot.dat", 'r')
    token = f.readline().split()[0]
    target_id = f.readline().split()[0]

    return [token, target_id]


[t, d] = get_token()
bot = telepot.Bot(t)


def set_bot(token):
    bot = telepot.Bot(token)
    return bot


def send_msg(bot, dt, msg):
    for m in msg:
        bot.sendMessage(dt, m)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='시작', callback_data='press'),
        InlineKeyboardButton(text='멈춰', callback_data='press')],
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