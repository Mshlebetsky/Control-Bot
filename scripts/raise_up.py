import pandas as pd
import os
from selenium.webdriver import Chrome,ChromeOptions,ChromeService
from selenium.webdriver.common.by import By
import time
from selenium import webdriver

import signal

def authorization(delay=1):
    safari_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
    my_login = 'Captain_BBPE'
    my_pass = '6234m1234M'

    # XPATH_change = ['//*[@id="t53323534"]/div[3]/a[1]/i']
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={safari_ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless=new')
    # options.add_argument('--headless=old')
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
def update_all_chapters(browser, chapters_urls, delay):
    for chapter in chapters_urls:
        update_single_chapter(browser, chapter, delay)
        time.sleep(2)
    return browser

def inf_upating(chapters_urls, delay_ = 1):
    count = 0
    delay = delay_
    browser = authorization()
    while delay < 50:
        # exit_check()
        time.sleep(delay)
        try:
            update_all_chapters(browser, chapters_urls, delay)
            count += 1
            print(f'run the {count}  time was   w successful')
            delay = delay_
        except:
            delay += 1
            print(f'Error with {delay} attemt')
    browser.close()
def close_window():
    browser = Chrome()
    browser.close()

