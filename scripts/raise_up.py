from selenium.webdriver import Chrome,ChromeOptions,ChromeService
from selenium.webdriver.common.by import By
import time
from selenium import webdriver


def get_chapter_urls():
    chapters_urls = []
    # file = open('../Data/urls_for_raise_up.txt', 'r', encoding='utf-8')
    file = open('Data/urls_for_raise_up.txt', 'r', encoding='utf-8')

    for line in file:
        # print(line)
        try:
            line = line.split(' ')[0]
        except:
            line = line
        if '\n' in line:
            line = line[:-1]
        chapters_urls.append(line)
    return chapters_urls
def authorization(delay=1):
    safari_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
    my_login = 'Captain_BBPE'
    my_pass = '6234m1234M'

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={safari_ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless=new')
    options.add_argument('--headless=old')
    options.add_argument("--window-size=1920,1080")
    try:
        browser = Chrome(options=options)
        main_url = 'https://tl.rulate.ru/'
        browser.get(main_url)
        time.sleep(delay)
        browser.find_element(By.XPATH, '/html/body/header/div/div[3]/div[2]/div/button').click()
    except:
        print('Error with downl. page')
        quit()
    try:
        for ch in my_login:
            browser.find_element(By.NAME, 'login[login]').send_keys(ch)
            time.sleep(0.01 * delay)
        for ch in my_pass:
            browser.find_element(By.NAME, 'login[pass]').send_keys(ch)
            time.sleep(0.01 * delay)
        browser.find_element(By.XPATH, '//*[@id="header-login"]/form/input[3]').click()
        time.sleep(delay)
        return browser
    except:
        print('Error with entering log/pass')
def update_single_chapter(browser, url, delay = 1, temp_delay = 5):
    browser.get(url)
    time.sleep(temp_delay * 0.5)
    browser.find_element(By.XPATH,"//*[@title='Редактировать перевод']").click()
    textarea = browser.find_element(By.NAME, 'Translation[body]')
#     print(textarea.text,, len(textarea.text))
    text_lenght = int(browser.find_element(By.ID,'tr-ccnt').find_elements(By.TAG_NAME, 'b')[1].text)
    if text_lenght > 100:
        textarea.clear()
        for ch in range(1, temp_delay + 2):
            textarea.send_keys(delay)
    else:
        textarea.send_keys(delay)
    time.sleep(temp_delay)
    browser.find_element(By.ID, 'sendTranslate').click()
    time.sleep(temp_delay)
    return(browser)
def update_all_chapters(browser, delay):
    chapters_urls = get_chapter_urls()
    for chapter in chapters_urls:
        update_single_chapter(browser, chapter, delay)
        time.sleep(2)
    return browser

def inf_upating(delay_ = 40, working_time_ = 5):
    delay = delay_
    browser = authorization()
    time_start = time.time()
    working_time = working_time_ * 60
    count = 0
    try:
        while (delay < (delay_ + 5)) and (time_start + working_time > time.time()):
            time.sleep(delay)
            count += 1
            try:
                update_all_chapters(browser, delay)
                print(f'run the {count}  time was successful')
                delay = delay_
            except:
                delay += 1
                print(f'Error with {count} attemt')
            # count += 1
        browser.close()
        return f'Обновлено {count} раз за {working_time} минут '
    except:
        return f'ошибка на {count} повторении'
# inf_upating(40, 2)
# print(get_chapter_urls())