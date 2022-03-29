import telepot
import os.path


def get_token():
    f = open(os.path.expanduser('~') + "/.telegram_bot.dat", 'r')
    token = f.readline().split()[0]
    to = f.readline().split()[0]

    return [token, to]


def set_bot(token):
    bot = telepot.Bot(token)
    return bot


def send_msg(bot, dt):
    bot.senMessage(dt, )