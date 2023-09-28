import csv 
import os 
import random
 
from django.conf import settings 
from django.core.management.base import BaseCommand
 
from autoservice.models import AutoService, Company, City, GeolocationAutoService
from core.utils import process_file
from csv import reader
 
 
class Command(BaseCommand): 
    """
    Импорт данных давтосервисов из CSV.
    """
    def handle(self, *args, **options) -> None: 
        csv: reader = process_file('service.csv')
        next(csv, None)

        obj_city: City = City.objects.filter(rus_name='Москва').first()
        for row in csv:
            obj_company: Company
            obj_geo: GeolocationAutoService
            obj_service: AutoService
            created: bool

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
                rating=row[8],
                votes=row[9],
                city=obj_city,
                openfrom=row[2],
                openuntil=row[3],
                site=row[6]
            ) 
        self.stdout.write('Импорт автосервсов прошел успешно.')