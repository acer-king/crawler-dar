FROM python:latest

WORKDIR /usr/app/
COPY ./src ./src
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
