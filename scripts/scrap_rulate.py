import csv
import multiprocessing
import os
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process, Manager
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# --------------------------------------------
# Настройки
# --------------------------------------------
NUM_BROWSERS = 12
CSV_FILE = "rulate_books.csv"
BASE_URL = "https://tl.rulate.ru/search/index/t//cat/0/rate_min/0/rate_max/5/rate_quality_min/0/rate_quality_max/5/s_lang/0/t_lang/0/adult/0/type/0/remove_machinelate/0/sort/4/genres_cond/0/tags_cond/0/fandoms_cond/0/fandoms_ex_all/0/n_chapters/0/n_chapters_max//atmosphere/0/Book_page/"

# --------------------------------------------
# Функция для сбора данных со страницы
# --------------------------------------------
def collect_data(driver):
    data = {}
    try:
        book_pages = driver.find_element(By.CLASS_NAME, "search-results").find_elements(By.TAG_NAME, "li")
    except NoSuchElementException:
        return data

    for book in book_pages:
        tokens = {"последняя активность:": "", "состояние перевода:": "", "жанры:": "", "тэги:": "", "фандомы:": ""}
        try:
            title = book.find_element(By.CLASS_NAME, "book-tooltip.tooltipstered").text
        except:
            continue

        if "/" in title:
            original_title, translated_title = title.split("/", 1)
        else:
            original_title, translated_title = title, ""

        try:
            link = book.find_element(By.CLASS_NAME, "book-tooltip.tooltipstered").find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "нет ссылки"

        labels = book.find_elements(By.CLASS_NAME, "label")
        chapters = labels[0].text.split("/")[0] if len(labels) > 0 else "0"
        total_pages = labels[1].text if len(labels) > 1 else "0"
        rating = labels[2].text if len(labels) > 2 else "0"
        likes = labels[-2].text if len(labels) >= 2 else "0"

        small_category = book.find_element(By.CLASS_NAME, "cat").text if book.find_elements(By.CLASS_NAME, "cat") else "нет категории"
        author_elements = book.find_elements(By.CLASS_NAME, "user.user-inactive")
        author_name = author_elements[0].text if author_elements else "нет автора"
        author_link = author_elements[0].get_attribute("href") if author_elements else "нет автора"

        description = ""
        try:
            for p in book.find_element(By.CLASS_NAME, "meta").find_elements(By.TAG_NAME, "p"):
                for token in tokens:
                    if p.text.startswith(token):
                        tokens[token] = p.text.replace(token, "").strip()
                        break
                else:
                    if ":" not in p.text[:25]:
                        description = p.text
        except:
            pass

        data[original_title] = [
            title, translated_title, link, chapters, total_pages, rating, likes,
            small_category, author_name, author_link,
            tokens["последняя активность:"],
            tokens["жанры:"], tokens["тэги:"], tokens["фандомы:"],
            tokens["состояние перевода:"], description
        ]

    return data


# --------------------------------------------
# Основная функция процесса
# --------------------------------------------
def worker(urls, existing_links, lock, process_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # создаем локальную копию ссылок (чтобы быстро проверять без блокировок)
    local_existing_links = set(existing_links.keys())

    for url in tqdm(urls, desc=f"PID {os.getpid()}", position=process_id):
        try:
            driver.get(url)
            time.sleep(1)
            books = collect_data(driver)
            with lock:
                with open("rulate_books.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    for key, values in books.items():
                        link = values[2]
                        if not link or link in local_existing_links:
                            continue
                        writer.writerow([key] + values)
                        existing_links[link] = True  # добавляем в менеджер
                        local_existing_links.add(link)
        except Exception as e:
            print(f"⚠️ Ошибка в процессе {os.getpid()}: {e}")
            continue

    driver.quit()




# --------------------------------------------
# Главная точка входа
# --------------------------------------------
if __name__ == "__main__":
    # Определяем общее количество страниц
    temp_driver = webdriver.Chrome()
    temp_driver.get(BASE_URL + "0")
    time.sleep(2)
    total_pages = temp_driver.find_element(By.CLASS_NAME, "span8").find_element(By.TAG_NAME, "h3").text.split(" ")[1]
    total_pages = int(total_pages) // 20 + 1
    temp_driver.quit()

    print(f"📄 Всего страниц: {total_pages}")

    urls = [f"{BASE_URL}{page}" for page in range(1, total_pages + 1)]
    # chunk_size = len(urls) // NUM_BROWSERS
    num_processes = NUM_BROWSERS
    chunk_size = len(urls) // num_processes
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    # Менеджер для межпроцессорного обмена
    manager = Manager()
    lock = manager.Lock()
    existing_links = manager.dict()  # используем dict, чтобы хранить ссылки как ключи


    # Если файл не существует — создаём и добавляем заголовки
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "original_title", "title", "translated_title", "link", "chapters",
                "total_pages", "rating", "likes", "category", "author_name", "author_link",
                "last_activity", "genres", "tags", "fandoms", "translation_status", "description"
            ])

    # Стартуем процессы
    processes = []
    for i in range(num_processes):
        urls_chunk = urls[i * chunk_size:(i + 1) * chunk_size]
        p = multiprocessing.Process(
            target=worker,
            args=(urls_chunk, existing_links, lock, i)
        )
        p.start()
        processes.append(p)
        print(f"🔹 Процесс {p.pid} запущен: {len(urls_chunk)} страниц")

    for p in processes:
        p.join()
    print("🎉 Все процессы завершены. Данные сохранены в rulate_books.csv")
