FROM python:3.5.1-onbuild

MAINTAINER Hamse

WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD python app.py

