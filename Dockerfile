# Используем официальный Python-образ
FROM python:3.11-slim

# Установим необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    xdg-utils \
    libglib2.0-0 \
    libgtk-3-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Установим Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Установим ChromeDriver через webdriver-manager (рекомендую вместо ручного скачивания)
RUN pip install --no-cache-dir selenium webdriver-manager python-dotenv

# Копируем код
WORKDIR /app
COPY . /app

# Запуск скрипта
CMD ["python", "scripts/raise_up.py"]
