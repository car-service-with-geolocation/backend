from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from autoservice.models import Job

User = get_user_model()


class Order(models.Model):
    """Модель заявки для авторизованного пользователя"""
    owner = models.ForeignKey(
        User,
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
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.owner} - {self.car},{self.task}'
