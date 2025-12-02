FROM python:3.12-slim

# -----------------------------
# 1. Устанавливаем зависимости ОС
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip xvfb gnupg libglib2.0-0 libnss3 libgconf-2-4 \
    libfontconfig1 libxrender1 libxi6 libxcursor1 libxss1 libxcomposite1 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 libcups2 libxdamage1 \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 2. Устанавливаем Python-зависимости
# -----------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 3. Копируем весь проект
# -----------------------------
COPY . .

# -----------------------------
# 4. Устанавливаем переменную окружения, чтобы UC работал с chromium
# -----------------------------
ENV UC_CHROME_BINARY=/usr/bin/chromium
ENV LANG=C.UTF-8

CMD ["python", "main.py"]
