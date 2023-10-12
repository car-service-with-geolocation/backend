from django.conf import settings
from django.db import models

from autoservice.models import Job
from users.models import CustomUser

class Order(models.Model):
    """Модель заявки для авторизованного пользователя"""
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Заказчик"
    )
    car = models.CharField(
        max_length=settings.MAX_LENGTH_CAR,
        verbose_name='Марка и модель автомобиля'
    )
    info = models.CharField(
        max_length=settings.MAX_LENGTH_INFO,
        verbose_name='Важная информация'
    )
    task = models.CharField(
        max_length=settings.MAX_LENGTH_TASK,
        verbose_name='Что случилось'
    )
    jobs = models.ManyToManyField(
        Job,
        related_name='orders', 
        verbose_name='Работы' 
    )
    image = models.ImageField(
        'Фото поломки',
        upload_to='order/images/',
        null=True,
    )

class Meta: 
        ordering = ('-pub_date', ) 
        verbose_name = 'Заявка' 
        verbose_name_plural = 'Заявки' 
 
def __str__(self): 
    return f'{self.owner} - {self.car},{self.task}'
