FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY ./app /app