import telebot
from dotenv import load_dotenv

from scripts.raise_up import  inf_upating
from scripts import get_comands
import os
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))
name = None
@bot.message_handler(commands=['start'])
def start(message):


    show_comands = get_comands.get_help()
    bot.send_message(message.chat.id, f'There is all comands \n{show_comands}')
@bot.message_handler(commands=['raise_up'])
def _func(message):
    bot.send_message(message.chat.id, f'Сколько минут будет работать бот?')
    bot.register_next_step_handler(message, raise_up_func_)
def raise_up_func_(message):
    try:
        working_time = int(message.text)
        bot.send_message(message.chat.id, f'Бот начинает работу на {working_time} минут')
    except:
        bot.send_message(message.chat.id, f'Ошибка ввода данных \n{type(message.text)}\n{message.text}')
        return 0
    try:
        reply_message = inf_upating(40, working_time)
        bot.send_message(message.chat.id, f'Бот закончил обновление\n{reply_message}')
    except:
        bot.send_message(message.chat.id, f'ошибка выполнения скрипта обновления')


if __name__ == '__main__':
    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=30,
    )