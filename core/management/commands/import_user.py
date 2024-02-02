import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


def process_file(name: str):
    with open(
        os.path.join(settings.BASE_DIR, 'static/data/', name),
        'r',
        encoding='utf-8'
    ) as file:
        return json.load(file)


class Command(BaseCommand):

    def handle(self, user_json=None, *args, **options):
        if user_json:
            data = process_file(user_json)
        else:
            data = process_file('user.json')
        for email, value in data.items():
            User.objects.get_or_create(
                email=email,
                password=value[0],
                first_name=value[1],
                phone_number=value[2]
            )
        print('-----Пользователи загружены!-----')
