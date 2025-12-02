import telebot
import sqlite3
from raise_up import  inf_upating
import get_comands
bot = telebot.TeleBot('7598997737:AAFZsXKy7NCQjklYSDVzda7QbwTRaRvkotM')
name = None
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('books_inf.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))'
    )
    conn.commit()
    cur.close()
    conn.close()


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



# bot.polling(non_stop=True)