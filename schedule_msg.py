import random
import time
import schedule
import telebot

from functions import text_gen
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
prediction = 'Ваше предсказание на сегодня✨:\n<i>' + text_gen.get_neuro_text(-1488, random.randint(1, 3) + 11) + '</i>'

f = open('./files/chats.txt', 'r', encoding='utf-8')
text = f.read()
arr = text.split('\n')
arr = arr[:len(arr) - 1]


def msg():
    try:
        i = 0
        for _ in arr:
            arr[i] = arr[i].rpartition(' - ')[0]
            bot.send_message(chat_id=arr[i], text=prediction, parse_mode='HTML')
            i += 1
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


schedule.every().day.at('08:00').do(msg)
while True:
    schedule.run_pending()
    time.sleep(1)
