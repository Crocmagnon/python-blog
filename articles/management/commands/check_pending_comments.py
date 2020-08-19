from django.conf import settings
from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.urls import reverse

from articles.models import Comment


class Command(BaseCommand):
    help = "Check for pending comments and send an email to the admin."

    def handle(self, *args, **options):
        count = Comment.objects.filter(status=Comment.PENDING).count()
        if count:
            url = reverse("admin:articles_comment_changelist")
            url = (settings.BLOG["base_url"] + url).replace(
                "//", "/"
            ) + "?status__exact=pending"
            message = f"There are {count} comments pending review.\n{url}"
            mail_admins("Comments pending", message)
