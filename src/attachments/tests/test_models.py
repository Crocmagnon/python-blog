from pathlib import Path

import pytest
from django.core.files import File

from attachments.models import Attachment


@pytest.mark.block_network()
@pytest.mark.vcr()
@pytest.mark.django_db()
def test_attachment_is_processed_by_shortpixel() -> None:
    # This path manipulation is required to make the test run from this directory
    # or from upper in the hierarchy (e.g.: settings.BASE_DIR)
    img_path = Path(__file__).parent / "resources" / "image.png"
    img_path = img_path.relative_to(Path.cwd())
    with Path(img_path).open("rb") as f:
        img_file = File(f)
        attachment = Attachment(description="test attachment", original_file=img_file)
        attachment.save()
