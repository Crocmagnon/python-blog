import pytest
from django.core.management import call_command


@pytest.mark.django_db()
def test_missing_migrations() -> None:
    call_command("makemigrations", "--check", "--dry-run")
