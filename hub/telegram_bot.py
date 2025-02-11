import telebot
from telebot.apihelper import ApiTelegramException
from telebot import types
import json
from config.creds import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

from logger import getLogger
log = getLogger(__name__)


TELE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
BOT = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@BOT.message_handler(commands=['start'])
def send_welcome(message):
    BOT.send_message(message.chat.id, f'Hello {message.from_user.full_name}')


@BOT.message_handler(commands=['test'])
def test_message(message):
    BOT.send_message(TELEGRAM_CHAT_ID,
                     text='test',
                     parse_mode='html'
                     )

def send_messages_by_telegram(messages):
    """
    Отправка messages пользователю с chat_id через Telegram
    :param messages:
    :return:
    """
    try:
        BOT.send_message(chat_id=TELEGRAM_CHAT_ID, text=messages, parse_mode='html')
    except ApiTelegramException as e:
        log.error('send_messages_by_telegram(): ApiTelegramException')

# BOT.polling(non_stop=True, interval=0)


def get_result():
    get_data = requests.get(TELE_URL)
    data_json = get_data.json()
    STATUS = data_json['ok']
    result = data_json['result']
    return result


def get_id_chat(key, result):
    for upd in result:
        if upd.get('message'):
            if upd.get('message').get('text') == key:
                return (upd['message']['chat']['id'])

