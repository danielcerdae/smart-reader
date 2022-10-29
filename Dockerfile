
FROM python:3.8.12-buster

WORKDIR /production

COPY .env .env
COPY smart_reader smart_reader
COPY model model
COPY requirements.txt requirements.txt
COPY setup.py setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn smart_reader.api.fast:app --host 0.0.0.0 --port $PORT



# A build time, download the model from the MLflow server and copy it once for all inside of the image

# RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv()); \
#     from taxifare.ml_logic.registry import load_model; load_model(save_copy_locally=True)'

# Then, at run time, load the model locally from the container instead of querying the MLflow server, thanks to "MODEL_TARGET=local"
# This avoids to download the heavy model from the Internet every time an API request is performed
# CMD MODEL_TARGET=local uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
