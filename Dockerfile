FROM python:3.10
ENV TelegramBotApi: "5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 insrall -r requarements
COPY . .
CMD ["python3", "main.py"]