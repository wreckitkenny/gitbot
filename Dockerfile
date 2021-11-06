FROM python

RUN mkdir -p /opt/gitbot
WORKDIR /opt/gitbot

COPY . /opt/gitbot

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "python3", "/opt/gitbot/gitbot.py", "-c", "/opt/gitbot/gitbot.conf" ]
