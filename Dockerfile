FROM python:3

ENV PYTHONDONTWROTEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /code

EXPOSE 8000

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "docker-entrypoint.sh" ]

