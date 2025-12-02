FROM python:3.11-slim

# Не спрашивать подтверждений
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем зависимости для Chrome и Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libu2f-udev \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libxrandr2 \
    libgbm1 \
    libxshmfence1 \
    libgtk-3-0 \
    libdrm2 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome Stable
RUN wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./chrome.deb \
    && rm chrome.deb

# Устанавливаем chromedriver под установленный Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9]+' | head -1) \
    && echo "Chrome major version: $CHROME_VERSION" \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}.0.0/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf /tmp/chromedriver*


# Создаем рабочую директорию
WORKDIR /app

# Устанавливаем Python зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . /app/

CMD ["python", "main.py"]
