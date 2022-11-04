
FROM python:3.8.12-buster

#WORKDIR /production

COPY .env .env
COPY smart_reader smart_reader
COPY model model
COPY requirements.txt requirements.txt
COPY setup.py setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install poppler-utils -y

CMD uvicorn smart_reader.api.main:app --host 0.0.0.0 --port $PORT
