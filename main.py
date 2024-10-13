import telebot
import webbrowser
from telebot import types
bot = telebot.TeleBot('7598997737:AAFZsXKy7NCQjklYSDVzda7QbwTRaRvkotM')
chapters_urls = ['https://tl.rulate.ru/book/119379/5032583',  # dnd and dxd
                 'https://tl.rulate.ru/book/95661/5032585',  # fairy tail
                 'https://tl.rulate.ru/book/119380/5032653']  # harem dxd
from scripts import raise_up
if __name__ == '__main__':
    # pid = os.getpid()
    # multiprocessing.Process(target=hook,args=[pid]).start() # НАЙТИ СПОСОБ ЗАКРЫТИЯ БРАУЗЕРА!!!
    raise_up.inf_upating(chapters_urls, 45)
    # close_window()
# @bot.message_handler(commands=['start'])
# def s
#
#
#
# @bot.message_handler(content_types=['photo'])
# def get_photo(message):
#     buttons = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Otsosi', url='https://pornhub.com')
#     btn2 = types.InlineKeyboardButton('Otsosal', callback_data='delete')
#     btn3 = types.InlineKeyboardButton('Uje', callback_data='edit')
#     buttons.row(btn1)
#     buttons.row(btn2,btn3)
#
#     bot.reply_to(message,'sosi', reply_markup = buttons)
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data == 'delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     elif callback.data == 'edit':
#         bot.edit_message_text('Sosniy',callback.message.chat.id, callback.message.message_id)
#
# bot.polling(non_stop=True)
