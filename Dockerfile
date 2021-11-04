FROM python3

RUN mkdir -p /opt/gitBot
WORKDIR /opt/gitBot

COPY . /opt/gitBot

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "python3", "/opt/gitBot/gitBot.py", "-c", "/opt/gitBot/gitBot.conf" ]
