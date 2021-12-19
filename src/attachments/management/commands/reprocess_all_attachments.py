from django.core.management.base import BaseCommand

from attachments.models import Attachment


class Command(BaseCommand):
    help = "Reprocess all attachments"

    def handle(self, *args, **options):
        for attachment in Attachment.objects.all():
            self.stdout.write(f"Processing {attachment}...")
            attachment.reprocess()
        self.stdout.write(self.style.SUCCESS("Successfully processed all attachments."))
