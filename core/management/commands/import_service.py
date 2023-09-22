import csv 
import os 
import random
 
from django.conf import settings 
from django.core.management.base import BaseCommand
 
from autoservice.models import AutoService, Company, City, GeolocationAutoService
 
 
def process_file(name: str): 
    return csv.reader(open(os.path.join( 
        settings.BASE_DIR, 'static/data/', name), 
        'r', encoding='utf-8'), delimiter=';') 
 
 
class Command(BaseCommand): 
 
    def handle(self, *args, **options): 
        # парсер базы данных 
        csv = process_file('service.csv')
        next(csv, None)
        obj_city = City.objects.filter(rus_name='Москва').first()
        for row in csv:
            obj_company, created = Company.objects.get_or_create(
                title=row[0],
                description=row[7]
            )
            obj_geo, created = GeolocationAutoService.objects.get_or_create(
                latitude=row[4],
                longitude=row[5]
            )
            obj_service, created = AutoService.objects.get_or_create( 
                company=obj_company,
                address=row[1],
                geolocation=obj_geo,
                rating=random.uniform(1, 10.0),
                votes=(1 + int(random.random() * 100)),
                city=obj_city,
                openfrom=row[2],
                openuntil=row[3],
                site=row[6]
            ) 
        print('парсер автосервисов прошел успешно')