FROM crocmagnon/blog
RUN pip install -r requirements-dev.txt
ENV TESTING "true"
WORKDIR /app
HEALTHCHECK none
# Required for pre-commit
RUN apt-get install -y git
COPY .git ./.git/

CMD ["/app/docker/runtests.sh"]
