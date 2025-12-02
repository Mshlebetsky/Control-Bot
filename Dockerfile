FROM python:3.12-slim

# Установка зависимостей для Chrome
RUN apt-get update && apt-get install -y\
wget\
gnupg\
unzip\
curl\
xvfb\
fonts-liberation\
libnss3\
libatk1.0-0\
libatk-bridge2.0-0\
libcups2\
libxcomposite1\
libxdamage1\
libxrandr2\
libxrender1\
libx11-xcb1\
libxcb1\
libxss1\
libasound2\
libappindicator3-1\
libgbm-dev\
xdg-utils\
&& rm -rf /var/lib/apt/lists/*

# Установка Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -\
&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list\
&& apt-get update\
&& apt-get install -y google-chrome-stable\
&& rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) &&\
LATEST=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") &&\
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip" &&\
unzip /tmp/chromedriver.zip -d /usr/local/bin/ &&\
rm /tmp/chromedriver.zip && chmod +x /usr/local/bin/chromedriver

WORKDIR /bot
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "main.py"]
