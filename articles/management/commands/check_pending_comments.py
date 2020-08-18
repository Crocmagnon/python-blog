from django.core.mail import mail_admins
from django.core.management import BaseCommand

from articles.models import Comment


class Command(BaseCommand):
    help = "Check for pending comments and send an email to the admin."

    def handle(self, *args, **options):
        count = Comment.objects.filter(status=Comment.PENDING)
        # url = reverse("admin:articles_comment_list")
        url = ""
        if count:
            message = f"There are {count} comments pending[0].\n[0]: {url}"
            mail_admins("Comments pending", message)
