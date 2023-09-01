from django.db import models
from django.conf import settings


class Transport(models.Model):
    brand = models.CharField( 
        max_length=settings.MAX_LENGTH_BRAND_NAME, 
        verbose_name='Бренд автомобиля' 
    ) 
    model = models.CharField( 
        max_length=settings.MAX_LENGTH_MODEL_NAME, 
        verbose_name='Модель автомобиля' 
    )

