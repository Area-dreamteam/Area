FROM python:3.13.7-alpine3.21

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

WORKDIR /server/app

RUN crontab -l

ENV ENV=dev

CMD crond && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --reload
