# Используем образ с Chrome и ChromeDriver
FROM selenium/standalone-chrome:latest

# Устанавливаем Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY main.py .
COPY scripts ./scripts
COPY Data ./Data
COPY scripts/get_comands.py .
COPY .env .

# Устанавливаем Python-зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python3", "main.py"]
