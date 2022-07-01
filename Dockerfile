FROM python:3

ENV PYTHONDONTWROTEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
COPY docker-entrypoint.sh /code/

RUN pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh

COPY . /code/


