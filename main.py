import telebot
from dotenv import load_dotenv
import os

from scripts.raise_up import inf_upating
from scripts import get_comands

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN не найден в .env")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        show_commands = get_comands.get_help()
        bot.send_message(message.chat.id, f"Список команд:\n{show_commands}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении команд: {e}")

@bot.message_handler(commands=['raise_up'])
def raise_up_prompt(message):
    bot.send_message(message.chat.id, "Сколько минут будет работать бот?")
    bot.register_next_step_handler(message, raise_up_handler)

def raise_up_handler(message):
    try:
        working_time = int(message.text)
        if working_time <= 0:
            raise ValueError("Время должно быть положительным числом")
    except ValueError:
        bot.send_message(message.chat.id, f"Ошибка ввода: '{message.text}' — введите целое число минут")
        return

    try:
        bot.send_message(message.chat.id, f"Бот начинает работу на {working_time} минут (запуск обновлений)...")
        result = inf_upating(delay_=40, working_time_=working_time)
        bot.send_message(message.chat.id, f"Бот закончил обновление:\n{result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка выполнения скрипта обновления: {e}")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
