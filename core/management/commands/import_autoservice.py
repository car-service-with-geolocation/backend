import json
import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from autoservice.models import (AutoService, AutoserviceJob, City, Company,
                                GeolocationAutoService, Job, Transport,
                                WorkingTime, WorkTimeRange)


def process_file(name: str):
    with open(os.path.join(settings.BASE_DIR, 'static/data/', name
                           ), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = process_file('avtoservice.json')
        count = 1
        for name_avtoservice, value in data.items():

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
                description=description_social
            )
            if created and value[8]:
                with open(
                    f'media/autoservice/images/logo/{name_avtoservice}.jpg',
                        'rb') as file:
                    image = ImageFile(file)
                    company.logo.save(f'{name_avtoservice}.jpg', image)

            #  Создаем GeolocationAutoService.
            geolocation, created = (
                GeolocationAutoService
                .objects
                .get_or_create(latitude=value[1][0], longitude=value[1][1])
            )

            #  Создаем WorkTimeRange.
            value_days = value[9]

            monday = value_days['Понедельник']
            if monday != 'Выходной':
                start_time, end_time = monday.split(" – ")
                monday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                monday_work = None

            tuesday = value_days['Вторник']
            if tuesday != 'Выходной':
                start_time, end_time = tuesday.split(" – ")
                tuesday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                tuesday_work = None

            wednesday = value_days['Среда']
            if wednesday != 'Выходной':
                start_time, end_time = wednesday.split(" – ")
                wednesday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                wednesday_work = None

            thursday = value_days['Четверг']
            if thursday != 'Выходной':
                start_time, end_time = thursday.split(" – ")
                thursday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                thursday_work = None

            friday = value_days['Пятница']
            if friday != 'Выходной':
                start_time, end_time = friday.split(" – ")
                friday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                friday_work = None

            saturday = value_days['Суббота']
            if saturday != 'Выходной':
                start_time, end_time = saturday.split(" – ")
                saturday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                saturday_work = None

            sunday = value_days['Воскресенье']
            if sunday != 'Выходной':
                start_time, end_time = sunday.split(" – ")
                sunday_work, created = WorkTimeRange.objects.get_or_create(
                    openfrom=start_time,
                    openuntil=end_time
                )
            else:
                sunday_work = None

            #  Создаем WorkingTime.
            workingtime, created = WorkingTime.objects.get_or_create(
                monday=monday_work,
                tuesday=tuesday_work,
                wednesday=wednesday_work,
                thursday=thursday_work,
                friday=friday_work,
                saturday=saturday_work,
                sunday=sunday_work,
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
                city=City.objects.get(id=507),
                working_time=workingtime,
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
                brand = item
                latin_cyrillic_dict = {
                    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
                    'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
                    'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'cz',
                    'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '',
                    'э': 'e', 'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B',
                    'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
                    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K',
                    'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
                    'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
                    'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '',
                    'Ы': 'y', 'Ь': '', 'Э': 'E', 'Ю': 'U', 'Я': 'YA', ',': '',
                    '?': '', ' ': '', '~': '', '!': '', '@': '', '#': '',
                    '$': '', '%': '', '^': '', '&': '', '*': '', '(': '',
                    ')': '', '-': '', '=': '', '+': '', ':': '', ';': '',
                    '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '',
                    '№': '', '[': '', ']': '', '{': '', '}': '', 'ґ': '',
                    'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i', 'Є': 'e', '—': '',
                    'Š': 's', 'š': 's'
                }
                for key in latin_cyrillic_dict:
                    item = item.replace(
                        key, latin_cyrillic_dict[key]).lower()
                transport, created = Transport.objects.get_or_create(
                    brand=brand.strip(),
                    slug=item
                )
                transport.autoservices.add(avtoservice)
            print(f'-------{count}--------{name_avtoservice}--------------OK')
            count += 1
        print('ЗАГРУЗКА АВТОСЕРВИСОВ ЗАВЕРШЕНА!')
