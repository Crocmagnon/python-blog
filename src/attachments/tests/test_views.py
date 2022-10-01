from pathlib import Path

import pytest
from django.core.files import File
from django.test.client import Client
from django.urls import reverse

from attachments.models import Attachment


@pytest.mark.block_network()
@pytest.fixture()
def attachment(db: None) -> Attachment:
    # This path manipulation is required to make the test run from this directory
    # or from upper in the hierarchy (e.g.: settings.BASE_DIR)
    original_path = Path(__file__).parent / "resources" / "image.png"
    original_path = original_path.relative_to(Path.cwd())
    processed_path = Path(__file__).parent / "resources" / "docker-logo.png"
    processed_path = processed_path.relative_to(Path.cwd())
    with original_path.open("rb") as of, processed_path.open("rb") as pf:
        original_file = File(of)
        processed_file = File(pf)
        attachment = Attachment.objects.create(
            description="Docker logo",
            original_file=original_file,
            processed_file=processed_file,
        )
        attachment.save()
    return attachment


def test_view_original(attachment: Attachment, client: Client) -> None:
    url = reverse("attachments:original", kwargs={"pk": attachment.pk})
    res = client.get(url)
    assert res.status_code == 302
    assert res.url == attachment.original_file.url


def test_view_processed(attachment: Attachment, client: Client) -> None:
    url = reverse("attachments:processed", kwargs={"pk": attachment.pk})
    res = client.get(url)
    assert res.status_code == 302
    assert res.url == attachment.processed_file.url
