from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from django.core.validators import RegexValidator
from autoservice.models import AutoService, Job

User = get_user_model()


class Order(models.Model):
    """Модель заявки для авторизованного пользователя"""

    STATUSES = [
        ("OPENED", "открыта"),
        ("COMPLETED", "выполнена"),
        ("CANCELED", "отменена"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик")
    car = models.CharField(
        max_length=settings.MAX_LENGTH_CAR, verbose_name="Марка и модель автомобиля"
    )
    info = models.CharField(
        max_length=settings.MAX_LENGTH_INFO,
        verbose_name="Важная информация",
        null=True,
    )
    task = models.CharField(
        max_length=settings.MAX_LENGTH_TASK,
        verbose_name="Что случилось",
        null=True,
    )
    jobs = models.ManyToManyField(
        Job,
        related_name="orders",
        verbose_name="Работы",
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=20,
        verbose_name="Статус заявки",
        choices=STATUSES,
        default=STATUSES[0][0],
    )
    autoservice = models.ForeignKey(
        AutoService,
        related_name="orders",
        verbose_name="Автосервис",
        on_delete=models.SET_NULL,
        null=True,
    )
    phone_number = models.CharField(
        max_length=settings.PHONE_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r'^(\+7|8)[0-9]{10}$',
                "Введите номер телефона в формате: '+79995553322'",
            )
        ],
        help_text="Введите номер телефона",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.owner} - {self.car},{self.task}"


class OrderImages(models.Model):
    file = models.FileField(
            "Фото поломки",
            upload_to="order/images/",
            null=True,
        )
    upload_date = models.DateTimeField(
        "Дата загрузки",
        auto_now_add=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="images",
        null=True,
    )

    class Meta:
        verbose_name = "Фото поломки"
        verbose_name_plural = "Фото поломки"

    def __str__(self) -> str:
        return f"{self.image}-{self.upload_date}"
