import time
from pathlib import Path

import requests
from invoke import task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
SRC_DIR = BASE_DIR / "src"


@task
def test(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run("pytest", pty=True, echo=True)


@task
def test_cov(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run(
            "pytest --cov=. --cov-report term-missing:skip-covered",
            pty=True,
            echo=True,
        )


@task
def pre_commit(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("pre-commit run --all-files", pty=True)


@task
def mypy(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("mypy src", pty=True)


@task(pre=[pre_commit, mypy, test_cov])
def check(ctx):
    pass


@task
def build(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("docker-compose build django", pty=True, echo=True)


@task
def publish(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("docker-compose push django", pty=True, echo=True)


@task
def deploy(ctx):
    ctx.run("ssh ubuntu /home/gaugendre/blog/update", pty=True, echo=True)


@task
def check_alive(ctx):
    for _ in range(5):
        try:
            res = requests.get("https://gabnotes.org")
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            time.sleep(1)
        return


@task(pre=[check, build, publish, deploy], post=[check_alive])
def beam(ctx):
    pass


@task
def download_db(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("scp ubuntu:/home/gaugendre/blog/db/db.sqlite3 ./db/db.sqlite3")
        ctx.run("rm -rf src/media/")
        ctx.run("scp -r ubuntu:/home/gaugendre/blog/media/ ./src/media")
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py two_factor_disable gaugendre", pty=True)
        ctx.run("./manage.py changepassword gaugendre", pty=True)
