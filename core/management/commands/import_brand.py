import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from autoservice.models import Transport


def process_file(name: str): 
    return csv.reader(open(os.path.join( 
        settings.BASE_DIR, 'static/data/', name), 
        'r', encoding='utf-8'), delimiter=',') 
 
 
class Command(BaseCommand): 
 
    def handle(self, *args, **options): 
        # парсер базы данных 
        csv = process_file('brand.csv') 
        #next(csv, None) 
        for row in csv:
            obj, created = Transport.objects.get_or_create( 
                brand=row[0], 
                slug=row[1]
            ) 
        print('парсер транспорта прошел успешно')