import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            "Subject here",
            "Here is the message.",
            None,
            ["ipad22855@gmail.com"],
            fail_silently=False,
        )
        print('Письмо отправлено')
