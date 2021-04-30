FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY . /app

# For puppeteer
RUN apt-get update -y \
    && xargs apt-get install -y < apt-packages.txt

RUN pip install -r requirements.txt

EXPOSE 80
