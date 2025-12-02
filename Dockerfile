FROM python:3.12-slim

# ----------------------------------------------------
# 1. Устанавливаем системные пакеты + зависимости Chrome
# ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg ca-certificates unzip xvfb \
    libglib2.0-0 libnss3 libx11-6 libx11-xcb1 libxcb1 libxcb-render0 \
    libxcb-shm0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxi6 \
    libxtst6 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 libatk1.0-0 \
    libatk-bridge2.0-0 libdrm2 libgbm1 libasound2 libxkbcommon0 \
    fonts-liberation libu2f-udev libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# 2. Добавляем Google Chrome репозиторий (корректный способ)
# ----------------------------------------------------
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
       | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] \
       http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list

# ----------------------------------------------------
# 3. Устанавливаем Chrome Stable
# ----------------------------------------------------
RUN apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# 4. Python зависимости
# ----------------------------------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# 5. Код приложения
# ----------------------------------------------------
COPY . .

# ----------------------------------------------------
# 6. Переменная для undetected-chromedriver
# ----------------------------------------------------
ENV UC_CHROME_BINARY=/usr/bin/google-chrome

CMD ["python", "main.py"]
