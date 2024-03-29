from typing import Any

from django.core.management.base import BaseCommand

from attachments.models import Attachment


class Command(BaseCommand):
    help = "Reprocess all attachments"  # noqa: A003

    def handle(self, *_args: Any, **_options: Any) -> None:
        for attachment in Attachment.objects.all():
            self.stdout.write(f"Processing {attachment}...")
            attachment.reprocess()
        self.stdout.write(self.style.SUCCESS("Successfully processed all attachments."))
