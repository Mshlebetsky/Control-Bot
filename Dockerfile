FROM python:3.12-slim

# Установка зависимостей для Chrome и Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# Установка ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+' | head -1) \
    && wget -q "https://chromedriver.storage.googleapis.com/$CHROME_VERSION.0.0/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Рабочая директория
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY main.py .
COPY scripts ./scripts
COPY Data ./Data
COPY scripts/get_comands.py .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем .env
COPY .env .

# Запуск бота
CMD ["python", "main.py"]
