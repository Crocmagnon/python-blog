FROM crocmagnon/blog
RUN pip install -r requirements-dev.txt
ENV TESTING "true"
WORKDIR /app
HEALTHCHECK none
CMD ["python", "-m", "pytest"]
