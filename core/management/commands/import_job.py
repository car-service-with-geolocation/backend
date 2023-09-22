import csv 
import os 
 
from django.conf import settings 
from django.core.management.base import BaseCommand 
 
from autoservice.models import Job
 
 
def process_file(name: str): 
    return csv.reader(open(os.path.join( 
        settings.BASE_DIR, 'static/data/', name), 
        'r', encoding='utf-8'), delimiter=',') 
 
 
class Command(BaseCommand): 
 
    def handle(self, *args, **options): 
        # парсер базы данных 
        csv = process_file('job.csv')
        for row in csv:
            obj, created = Job.objects.get_or_create( 
                title=row[0],
            ) 
        print('парсер видов работ прошел успешно')
