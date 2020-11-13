FROM python:3.6
LABEL maintainer @nataliasudar

RUN apt-get -qq -y update
RUN apt-get -y install telnet vim && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/code
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY code/* ./
RUN cd /opt/env/ && export $(grep -v '^#' .env | xargs)

RUN useradd app
RUN chown app:app -R ../code

CMD python3 app.py && python3 app_flask.py
