FROM python:3.12-slim

# Обновление системы и установка зависимостей Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libnss3 \
    libasound2 \
    libgbm1 \
    libxshmfence1 \
    libx11-xcb1 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome (через .deb, без apt-key)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb && \
    apt-get update && apt-get install -y /tmp/chrome.deb && \
    rm /tmp/chrome.deb

# Установка ChromeDriver, совпадающего с Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+\.\d+") && \
    MAJOR=$(echo $CHROME_VERSION | cut -d '.' -f 1) && \
    wget -O /tmp/chromedriver.zip \
        "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/*

# Установка питон-пакетов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
