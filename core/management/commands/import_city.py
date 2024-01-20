from csv import reader

from django.conf import settings
from django.core.management.base import BaseCommand

from autoservice.models import City, GeolocationCity
from core.utils import process_file


class Command(BaseCommand):
    """
    Импорт данных городов РФ из CSV файла.
    """
    def handle(self, cities_csv=None, *args, **options):
        if cities_csv:
            csv = process_file(cities_csv)
        else:
            csv = process_file('russia_city.csv')
        next(csv, None)

        for row in csv:
            obj_geo: GeolocationCity
            obj_city: City
            created: bool

            obj_geo, created = GeolocationCity.objects.get_or_create(
                latitude=row[1],
                longitude=row[2]
            )
            obj_city, created = City.objects.get_or_create(
                rus_name=row[0],
                geolocation=obj_geo
            )
        self.stdout.write('Импорт данных городов прошел успешно.')
