from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

from users.models import CustomUser as User


class Transport(models.Model):
    """
    Модель для базы данных брендов/моделей авто
    """

    brand = models.CharField(
        max_length=settings.MAX_LENGTH_TRANSPORT_BRAND,
        verbose_name='Название бренда'
    )
    slug = models.CharField(
        max_length=settings.MAX_LENGTH_TRANSPORT_SLUG,
        verbose_name='Уникальный Slug'
    )
    # model = models.CharField(
    #     max_length=settings.MAX_LENGTH_TRANSPORT_MODEL,
    #     verbose_name='Название модели'
    # )
    # image = models.ImageField(
    #     'Изображение автомобиля',
    #     upload_to='transports/'
    # )

    class Meta:
        ordering = ('brand', )
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        # constraints = [models.UniqueConstraint(
        #                fields=('brand', 'model'),
        #                name='unique_transport')]

    def __str__(self):
        return f'{self.brand}'


class Cars(models.Model):
    """
    Модель с общей информацией об автомобиле
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Владелец'
    )
    car = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
        verbose_name='Автомобиль'
    )
    color = ColorField(
        default='#FFFFFF',
        verbose_name='Цвет автомобиля'
    )
    vin = models.CharField(
        max_length=settings.MAX_LENGTH_VIN,
        verbose_name='VIN-номер автомобиля'
    )
    number_of_car = models.CharField(
        max_length=settings.MAX_LENGTH_NUMBER_OF_CAR,
        verbose_name='Гос.номер автомобиля'
    )
    odometr = models.CharField(
        max_length=settings.MAX_LENGTH_ODOMETR,
        verbose_name='Пробег автомобиля'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год приобретения автомобиля'
    )
    last_service_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата последнего ТО'
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.car}, {self.number_of_car}'
