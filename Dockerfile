FROM python:3.10.10

WORKDIR /home/Dropbox_API

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
