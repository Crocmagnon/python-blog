FROM ubuntu:latest as git
RUN apt-get update \
    && apt-get install -y git \
    && mkdir /app

ADD . /app
WORKDIR /app
RUN git rev-parse HEAD | tee /version

FROM python:3.8.5-slim

RUN apt-get update \
    && apt-get install -y curl \
    && echo "Europe/Paris" > /etc/timezone \
    && mkdir /app && mkdir /db

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY manage.py LICENSE .pre-commit-config.yaml pyproject.toml requirements-dev.txt ./
COPY docker ./docker/
COPY blog ./blog/
COPY attachments ./attachments/
COPY articles ./articles/
COPY --from=git /version /app/.version

ENV SECRET_KEY "changeme"
ENV DEBUG "false"
ENV HOST ""
ENV DB_BASE_DIR "/db"

HEALTHCHECK --start-period=30s CMD curl -f http://localhost:8000

CMD ["/app/docker/run.sh"]
