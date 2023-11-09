FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip3 install pyTelegramBotAPI
RUN pip3 install pytz
RUN pip3 install openai

CMD [ "python3", "main.py" ]

