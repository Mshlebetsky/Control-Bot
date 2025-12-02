import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Загружаем .env
load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

DATA_DIR = os.path.join(os.getcwd(), "Data")  # рабочая директория в контейнере


def get_chapter_urls():
    file_path_1 = os.path.join(DATA_DIR, 'urls_for_raise_up.txt')
    chapters_urls = []
    try:
        with open(file_path_1, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split(' ')[0].strip()
                if line:
                    chapters_urls.append(line)
        return chapters_urls
    except Exception as e:
        print(f"Error reading URLs file: {e}")
        return []


def authorization(delay=1.5):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        browser = webdriver.Chrome(options=options)
        print("Браузер запущен")
    except Exception as e:
        print(f"Ошибка запуска браузера: {e}")
        return None, False

    try:
        main_url = 'https://tl.rulate.ru/'
        browser.get(main_url)
        time.sleep(delay)
        browser.find_element(By.XPATH, '/html/body/header/div/div[3]/div[2]/div/button').click()
    except Exception as e:
        print(f"Ошибка при открытии страницы: {e}")
        return browser, False

    try:
        for ch in LOGIN:
            browser.find_element(By.NAME, 'login[login]').send_keys(ch)
            time.sleep(0.01 * delay)
        for ch in PASSWORD:
            browser.find_element(By.NAME, 'login[pass]').send_keys(ch)
            time.sleep(0.01 * delay)
        browser.find_element(By.XPATH, '//*[@id="header-login"]/form/input[3]').click()
        time.sleep(delay)
        return browser, True
    except Exception as e:
        print(f"Ошибка ввода логина/пароля: {e}")
        return browser, False


def update_single_chapter(browser, url, delay=1, temp_delay=5):
    try:
        browser.get(url)
        time.sleep(temp_delay * 0.5)
        browser.find_element(By.XPATH, "//*[@title='Редактировать перевод']").click()
        textarea = browser.find_element(By.NAME, 'Translation[body]')
        text_length = int(browser.find_element(By.ID, 'tr-ccnt').find_elements(By.TAG_NAME, 'b')[1].text)
        if text_length > 100:
            textarea.clear()
            for _ in range(temp_delay + 1):
                textarea.send_keys(delay)
        else:
            textarea.send_keys(delay)
        time.sleep(temp_delay)
        browser.find_element(By.ID, 'sendTranslate').click()
        time.sleep(temp_delay)
    except Exception as e:
        print(f"Ошибка обновления главы {url}: {e}")
    return browser


def update_all_chapters(browser, delay):
    chapters_urls = get_chapter_urls()
    for chapter in chapters_urls:
        browser = update_single_chapter(browser, chapter, delay)
        time.sleep(2)
    return browser


def inf_upating(delay_=40, working_time_=5):
    delay = delay_
    browser, success = authorization()
    if not success:
        return "Ошибка авторизации"

    print("Авторизация прошла успешно")
    print("Начало обновлений...")
    time_start = time.time()
    working_time = working_time_ * 60
    count = 0
    try:
        while (delay < (delay_ + 5)) and (time_start + working_time > time.time()):
            time.sleep(delay)
            try:
                update_all_chapters(browser, delay)
                print(f"{count + 1} круг обновлений прошел успешно")
                delay = delay_
            except Exception as e:
                delay += 1
                print(f"Ошибка на {count + 1} повторении: {e}")
            count += 1
        browser.close()
        return f"Обновлено {count} раз за {working_time // 60} минут"
    except Exception as e:
        return f"Ошибка на {count} повторении: {e}"
