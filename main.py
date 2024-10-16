from scripts import Bot
# bot = telebot.TeleBot('7598997737:AAFZsXKy7NCQjklYSDVzda7QbwTRaRvkotM')
# Bot()
chapters_urls = []
file = open('Data/urls_for_raise_up.txt', 'r', encoding='utf-8')
for line in file:
    print(line)
    if '\n' in line:
        line = line[:-1]
    chapters_urls.append(line)
working_time = int(input('Введи количество минут выполнения'))
if __name__ == '__main__':
    # raise_up.inf_upating(chapters_urls, 45, working_time)
    print(1)
