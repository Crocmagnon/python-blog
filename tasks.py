from pathlib import Path

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


@task(pre=[build, publish, deploy])
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
