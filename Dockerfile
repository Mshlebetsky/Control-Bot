# Используем официальный Python 3.12 slim
FROM python:3.12-slim

# ----------------------------------------------------
# Установка необходимых утилит и Chrome
# ----------------------------------------------------
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Добавляем репозиторий Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем ChromeDriver через wget
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# ----------------------------------------------------
# Рабочая директория
# ----------------------------------------------------
WORKDIR /app

# Копируем проект
COPY . /app

# ----------------------------------------------------
# Устанавливаем зависимости Python
# ----------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir selenium python-dotenv

# ----------------------------------------------------
# Переменные окружения (по желанию)
# ----------------------------------------------------
# ENV LOGIN=your_login
# ENV PASSWORD=your_password

# ----------------------------------------------------
# Команда запуска
