from django.conf import settings
from django.db import models


class Jobs(models.Model): 
    """Модель работ""" 
    name = models.CharField( 
        max_length=settings.MAX_LENGTH_JOBS_NAME, 
        verbose_name='Название работы' 
    ) 
    description = models.CharField( 
        max_length=settings.MAX_LENGTH_JOBS_DESCRIPTION, 
        verbose_name='Описание работы' 
    ) 
    price =  models.CharField( 
        max_length=settings.MAX_LENGTH_JOBS_PRICE, 
        verbose_name='Относительная стоимость работ' 
    )
    slug =  models.CharField( 
        max_length=settings.MAX_LENGTH_JOBS_SLUG, 
        verbose_name='Уникальный Slug' 
    )

    class Meta: 
        ordering = ('name', ) 
        verbose_name = 'Работа' 
        verbose_name_plural = 'Работы' 
 
    def __str__(self): 
        return f'{self.name}, {self.description}, {self.price}, {self.slug}' 
