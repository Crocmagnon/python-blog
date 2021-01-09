import pytest
from django.test import Client
from django.urls import reverse

from articles.models import User


@pytest.mark.django_db
@pytest.mark.flaky(reruns=5, reruns_delay=3)
def test_can_access_add_article(client: Client, author: User):
    client.force_login(author)
    res = client.get(reverse("admin:articles_article_add"))
    assert res.status_code == 200
