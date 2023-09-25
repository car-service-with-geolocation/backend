import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from autoservice.models import City, GeolocationCity


def process_file(name: str):
    return csv.reader(open(os.path.join(
        settings.BASE_DIR, 'static/data/', name
        ), 'r', encoding='utf-8'), delimiter=',')


class Command(BaseCommand):

    def handle(self, *args, **options):
        '''Парсим города с координатами.'''
        csv = process_file('russia_city.csv')
        next(csv, None)
        for row in csv:
            obj_geo, created = GeolocationCity.objects.get_or_create(
                latitude=row[1],
                longitude=row[2]
            )
            obj_city, created = City.objects.get_or_create(
                rus_name=row[0],
                geolocation=obj_geo
            )
        print('---parsing city is OK!---')
