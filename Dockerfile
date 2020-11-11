## Build venv
FROM python:3.8.6-buster AS venv

# https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.0.10
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH /root/.poetry/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/root/.poetry/lib

WORKDIR /app
COPY pyproject.toml poetry.lock ./
# Will install dev deps as well, so that we can run tests in this image
RUN python -m venv --copies /app/venv \
    && . /app/venv/bin/activate \
    && poetry config cache-dir /app/poetry-cache \
    && (python -c "from poetry.factory import Factory; l = Factory().create_poetry('.').locker; exit(0) if l.is_locked() and l.is_fresh() else exit(1)" \
            && echo "poetry.lock is up to date") \
        || (>&2 echo "poetry.lock is outdated. Run `poetry lock` on your machine and commit the file." && exit 1) \
    && poetry install --no-dev


## Get git versions
FROM alpine/git:v2.26.2 AS git
ADD . /app
WORKDIR /app
RUN git rev-parse HEAD | tee /version


## Beginning of runtime image
FROM python:3.8.6-slim-buster as prod

RUN echo "Europe/Paris" > /etc/timezone \
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


## Build venv for tests
FROM venv as venv-tests
WORKDIR /app
RUN . /app/venv/bin/activate \
    && poetry install


## Build test image
FROM prod as tests
RUN apt-get update && apt-get install -y --no-install-recommends git
COPY --from=venv-tests /app/venv /app/venv/
COPY .git ./.git/
