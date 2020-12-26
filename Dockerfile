## Build venv
FROM python:3.8.6-buster AS venv

# https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH /root/.poetry/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/root/.poetry/lib
ARG POETRY_OPTIONS

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m venv --copies /app/venv \
    && . /app/venv/bin/activate \
    && poetry config cache-dir /app/poetry-cache \
    && poetry install $POETRY_OPTIONS


## Get git versions
FROM alpine/git:v2.26.2 AS git
ADD . /app
WORKDIR /app
RUN git rev-parse HEAD | tee /version


## Beginning of runtime image
FROM python:3.8.6-slim-buster as prod

RUN apt-get update \
    # Git is required for pre-commit checks
    && apt-get install -y --no-install-recommends git \
    && echo "Europe/Paris" > /etc/timezone \
    && mkdir /db

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY manage.py LICENSE .pre-commit-config.yaml pyproject.toml ./
COPY docker ./docker/
COPY blog ./blog/
COPY attachments ./attachments/
COPY articles ./articles/
COPY --from=git /version /app/.version

ENV SECRET_KEY "changeme"
ENV DEBUG "false"
ENV HOST ""
ENV DB_BASE_DIR "/db"

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["/app/docker/run.sh"]
