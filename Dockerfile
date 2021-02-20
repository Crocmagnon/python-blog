## Build venv
FROM python:3.8.8-buster AS venv

# https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH /root/.poetry/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/root/.poetry/lib
ARG POETRY_OPTIONS

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmemcached-dev

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
FROM python:3.8.8-slim-buster as prod

RUN echo "Europe/Paris" > /etc/timezone \
    && mkdir /db

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmemcached-dev

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY manage.py LICENSE pyproject.toml ./
COPY docker ./docker/
COPY blog ./blog/
COPY attachments ./attachments/
COPY articles ./articles/
COPY --from=git /version /app/.version

ENV SECRET_KEY "changeme"
ENV DEBUG "false"
ENV DB_BASE_DIR "/db"
#ENV HOSTS="host1;host2"
#ENV ADMINS='Full Name,email@example.com'
#ENV MAILGUN_API_KEY='key-yourapikey'
#ENV MAILGUN_SENDER_DOMAIN='mailgun.example.com'
#ENV BLOG_BASE_URL='https://url-of-your-blog.example.com'
#ENV SHORTPIXEL_API_KEY='YOURAPIKEY'
#ENV SHORTPIXEL_RESIZE_WIDTH='750'
#ENV SHORTPIXEL_RESIZE_HEIGHT='10000'
#ENV PLAUSIBLE_DOMAIN='url-of-your-blog.example.com'
#ENV GOATCOUNTER_DOMAIN='blog.goatcounter.example.com'
#ENV MEMCACHED_LOCATION='memcached:11211'

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["/app/docker/run.sh"]
