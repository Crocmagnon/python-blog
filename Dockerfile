FROM python:3.8.5-slim

RUN apt-get update && apt-get install -y curl
RUN mkdir /app && mkdir /db
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY manage.py ./
COPY articles ./articles/
COPY blog ./blog/
COPY docker ./docker/

ENV SECRET_KEY "changeme"
ENV DEBUG "false"
ENV HOST ""
ENV DB_BASE_DIR "/db"

HEALTHCHECK --start-period=30s CMD curl -f http://localhost:8000

CMD ["/app/docker/run.sh"]
