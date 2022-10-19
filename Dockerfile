## Build venv
FROM python:3.11.0rc2-bullseye AS venv

# https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.1.15
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH /root/.local/bin:$PATH
ARG POETRY_OPTIONS

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python -m venv --copies /app/venv \
    && . /app/venv/bin/activate \
    && poetry install $POETRY_OPTIONS \
    && python -m pip install setuptools

ENV PATH /app/venv/bin:$PATH
COPY src ./src/
RUN python ./src/manage.py collectstatic --no-input

## Get git versions
FROM alpine/git AS git
ADD . /app
WORKDIR /app
RUN git rev-parse HEAD | tee /version


## Beginning of runtime image
FROM python:3.11.0rc2-slim-bullseye as prod
ENV TZ "Europe/Paris"
RUN mkdir /db

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY LICENSE pyproject.toml ./
COPY docker ./docker/
COPY src ./src/
COPY --from=git /version /app/.version
COPY --from=venv /app/src/staticfiles /app/src/staticfiles/

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
#ENV GOATCOUNTER_DOMAIN='blog.goatcounter.example.com'

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

WORKDIR /app/src
CMD ["/app/docker/run.sh"]
