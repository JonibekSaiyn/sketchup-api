FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install python-telegram-bot requests

CMD ["python", "bot.py"]
