import time
from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
SRC_DIR = BASE_DIR / "src"
COMPOSE_BUILD_FILE = BASE_DIR / "docker-compose-build.yaml"
COMPOSE_BUILD_ENV = {"COMPOSE_FILE": COMPOSE_BUILD_FILE}


@task
def update_dependencies(ctx: Context, *, sync: bool = True) -> None:
    return compile_dependencies(ctx, update=True, sync=sync)


@task
def compile_dependencies(
    ctx: Context,
    *,
    update: bool = False,
    sync: bool = False,
) -> None:
    common_args = "-q --allow-unsafe --resolver=backtracking"
    if update:
        common_args += " --upgrade"
    with ctx.cd(BASE_DIR):
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --strip-extras -o constraints.txt requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements-dev.in",
            pty=True,
            echo=True,
        )
    if sync:
        sync_dependencies(ctx)


@task
def sync_dependencies(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("pip-sync requirements.txt requirements-dev.txt", pty=True, echo=True)


@task
def test(ctx: Context) -> None:
    with ctx.cd(SRC_DIR):
        ctx.run("pytest", pty=True, echo=True)


@task
def test_cov(ctx: Context) -> None:
    with ctx.cd(SRC_DIR):
        ctx.run(
            "pytest --cov=. --cov-branch --cov-report term-missing:skip-covered",
            pty=True,
            echo=True,
            env={"COVERAGE_FILE": BASE_DIR / ".coverage"},
        )


@task
def pre_commit(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("pre-commit run --all-files", pty=True, echo=True)


@task
def mypy(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("pre-commit run --all-files mypy", pty=True)


@task(pre=[pre_commit, test_cov])
def check(_ctx: Context) -> None:
    pass


@task
def build(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run(
            "docker-compose build django",
            pty=True,
            echo=True,
            env=COMPOSE_BUILD_ENV,
        )


@task
def publish(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run(
            "docker-compose push django",
            pty=True,
            echo=True,
            env=COMPOSE_BUILD_ENV,
        )


@task
def deploy(ctx: Context) -> None:
    ctx.run("ssh ubuntu /mnt/data/blog/update", pty=True, echo=True)


@task
def check_alive(_ctx: Context) -> None:
    import requests

    exception = None
    for _ in range(5):
        try:
            res = requests.get("https://gabnotes.org", timeout=5)
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            time.sleep(2)
            exception = e
        else:
            print("Server is up & running")  # noqa: T201
            return
    msg = "Failed to reach the server"
    raise RuntimeError(msg) from exception


@task(pre=[check, build, publish, deploy], post=[check_alive])
def beam(_ctx: Context) -> None:
    pass


@task
def download_db(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("scp ubuntu:/mnt/data/blog/db/db.sqlite3 ./db/db.sqlite3")
        ctx.run("rm -rf src/media/")
        ctx.run("scp -r ubuntu:/mnt/data/blog/media/ ./src/media")
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py two_factor_disable gaugendre", pty=True)
        ctx.run("./manage.py changepassword gaugendre", pty=True)
