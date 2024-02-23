import json
import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from autoservice.models import (AutoService, AutoserviceJob, City, Company,
                                GeolocationAutoService, Job, Transport,
                                WorkingTime)


def process_file(name: str):
    with open(
        os.path.join(settings.BASE_DIR, 'static/data/', name),
        'r',
        encoding='utf-8'
    ) as file:
        return json.load(file)


class Command(BaseCommand):

    def handle(self, avtoservices_json=None, *args, **options):
        if avtoservices_json:
            data = process_file(avtoservices_json)
        else:
            data = process_file('avtoservice.json')
        count = 1
        for name_avtoservice, value in data.items():
            print(f'----{count}-----{name_avtoservice}-------пробую загрузить')

            #  Создаем Company.
            if len(value[5]) > 0:
                description_social = (
                    str(value[5])
                    .replace('[', '')
                    .replace(']', '')
                    .replace("'", '')
                )
            else:
                description_social = None
            company, created = Company.objects.get_or_create(
                title=name_avtoservice,
                description=description_social,
                legal_address="Москва, Красная площадь, д.1",
                taxpayer_id="0123456789"
            )
            if created and value[8]:
                try:
                    with open(
                        f'static/data/logo_autoservice/{name_avtoservice}.jpg',
                            'rb') as file:
                        image = ImageFile(file)
                        company.logo.save(f'{name_avtoservice}.jpg', image)
                except:
                    pass

            #  Создаем GeolocationAutoService.
            geolocation, created = (
                GeolocationAutoService
                .objects
                .get_or_create(latitude=value[1][0], longitude=value[1][1])
            )

            #  Создаем AutoService.
            if value[2]:
                phone_number = value[2]
                phone_number = (
                    phone_number
                    .replace("(", "")
                    .replace(")", "")
                    .replace("-", "")
                    .replace(" ", "")
                    [:12]
                )
            else:
                phone_number = None
            if not value[3]:
                value[3] = 'Москва'
            avtoservice, created = AutoService.objects.get_or_create(
                company=company,
                address=value[3],
                geolocation=geolocation,
                city=City.objects.get(id=2),
                phone_number=phone_number,
                site=value[4]
            )

            #  Создаем Job.
            for item in value[6]:
                job, created = Job.objects.get_or_create(
                    title=item
                )
                AutoserviceJob.objects.get_or_create(
                    service=avtoservice,
                    job=job
                )

            #  Создаем Transport.
            for item in value[7]:
                transport, created = Transport.objects.get_or_create(
                    brand=item.strip()
                )
                transport.autoservices.add(avtoservice)

            #  Создаем WorkingTime.
            if value[9]:
                for day_week, time in value[9].items():
                    workingtime, created = WorkingTime.objects.get_or_create(
                        day=day_week,
                        time=time
                    )
                    workingtime.autoservices.add(avtoservice)

            print(f'----{count}-----{name_avtoservice}-------загружено')
            count += 1
        print()
        print('ЗАГРУЗКА АВТОСЕРВИСОВ ЗАВЕРШЕНА!')
