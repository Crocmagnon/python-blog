# Blog

![Publish](https://github.com/Crocmagnon/blog/actions/workflows/publish.yaml/badge.svg)
![CodeQL](https://github.com/Crocmagnon/blog/actions/workflows/codeql-analysis.yaml/badge.svg)

Simple blog management system.

Hosted at https://gabnotes.org

## Development
```shell
pip install -U pip pip-tools invoke
inv sync-dependencies
pre-commit install --install-hooks
inv test-cov
./src/manage.py migrate
./src/manage.py createsuperuser
```

# Reuse
If you do reuse my work, please consider linking back to this repository 🙂
