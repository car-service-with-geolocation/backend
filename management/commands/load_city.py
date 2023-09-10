import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from autoservice.models import City


def process_file(name: str):
    return csv.reader(open(os.path.join(
        settings.BASE_DIR, 'static/data/', name
        ), 'r', encoding='utf-8'), delimiter=',')


class Command(BaseCommand):

    def handle(self, *args, **options):
        '''Парсим города с координатами.'''
        csv = process_file('koord_russia.csv')
        next(csv, None)
        for row in csv:
            obj, created = City.objects.get_or_create(
                rus_name=row[0],
                latitude=row[3],
                longitude=row[4]
            )
        print('---parsing city is OK!---')
