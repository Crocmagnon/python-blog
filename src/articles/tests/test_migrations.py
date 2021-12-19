import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_missing_migrations():
    call_command("makemigrations", "--check")
