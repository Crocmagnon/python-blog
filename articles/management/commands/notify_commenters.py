from collections import defaultdict

from django.conf import settings
from django.core.mail import mail_admins, send_mass_mail
from django.core.management import BaseCommand
from django.db.models import Q
from django.template import Context, Engine
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ngettext

from articles.models import Comment


class Command(BaseCommand):
    help = "Check for pending comments and send an email to the admin."

    def handle(self, *args, **options):
        to_notify = (
            Comment.objects.filter(
                Q(status=Comment.APPROVED) | Q(status=Comment.REJECTED),
                user_notified=False,
            )
            .exclude(email=None)
            .exclude(email="")
        )
        by_email = {}
        for comment in to_notify:
            if comment.email not in by_email:
                by_email[comment.email] = {"approved": [], "rejected": []}
            if comment.status == Comment.APPROVED:
                by_email[comment.email]["approved"].append(comment)
            elif comment.status == Comment.REJECTED:
                by_email[comment.email]["rejected"].append(comment)

        email_data = []
        for email, comments in by_email.items():
            approved = comments["approved"]
            rejected = comments["rejected"]
            subject = ngettext(
                "Your comment has been moderated.",
                "Your comments have been moderated.",
                len(approved) + len(rejected),
            )
            blog_title = settings.BLOG["title"]
            message = render_to_string(
                "articles/comments_notification_email.txt",
                {"approved": approved, "rejected": rejected, "blog_title": blog_title},
            ).replace("&#x27;", "'")
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            email_data.append((subject, message, from_email, recipient_list))
        send_mass_mail(tuple(email_data))
        to_notify.update(user_notified=True)
