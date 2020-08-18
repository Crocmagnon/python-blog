import pytest

from articles.models import User


@pytest.fixture()
@pytest.mark.django_db
def author():
    return User.objects.create_user("gaugendre")
