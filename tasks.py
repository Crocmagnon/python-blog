from pathlib import Path

from invoke import task

BASE_DIR = Path(__file__).parent.resolve(strict=True)


@task
def test(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("pytest", pty=True, echo=True)


@task
def test_cov(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run(
            "pytest --cov=. --cov-report term-missing:skip-covered",
            pty=True,
            echo=True,
        )


@task
def publish(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("docker-compose build django", pty=True, echo=True)
        ctx.run("docker-compose push django", pty=True, echo=True)


@task
def deploy(ctx):
    ctx.run("ssh ubuntu /home/gaugendre/blog/update", pty=True, echo=True)
