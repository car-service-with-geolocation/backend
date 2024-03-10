from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from core.validators import phone_number_validator, validate_all_isdigit
from users.models import CustomUser

User = get_user_model()


class Transport(models.Model):
    """Модель брендов (моделей) автомобилей."""

    brand = models.CharField(
        max_length=settings.MAX_LENGTH_TRANSPORT_BRAND,
        verbose_name="Название бренда",
    )

    class Meta:
        ordering = ("brand",)
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return f"{self.brand}"


class WorkingTime(models.Model):
    """Модель - режим работы автосервиса в определенный день недели."""

    DAY_CHOICES = (
        ("Monday", "Понедельник"),
        ("Tuesday", "Вторник"),
        ("Wednesday", "Среда"),
        ("Thursday", "Четверг"),
        ("Friday", "Пятница"),
        ("Saturday", "Суббота"),
        ("Sunday", "Воскресенье"),
    )
    day = models.CharField(
        max_length=255, choices=DAY_CHOICES, verbose_name="День недели"
    )
    time = models.CharField(
        max_length=255,
        verbose_name="Время работы в определенный день недели",
        validators=[
            RegexValidator(
                regex=r"^(\d{2}:\d{2} - \d{2}:\d{2}|Выходной)$",
                message=('Введите время в формате "ЧЧ:ММ - ЧЧ:ММ" или "Выходной".'),
            )
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["day", "time"], name="unique_day_time")
        ]
        verbose_name = "Режим работы в определенный день недели"
        verbose_name_plural = "Режимы работы в определенные дни недели"

    def __str__(self) -> str:
        return f"Режим работы {self.id}"


class GeolocationCity(models.Model):
    """Модель с геолокацией городов."""

    latitude = models.FloatField(
        verbose_name="Значение северной широты на карте",
    )
    longitude = models.FloatField(
        verbose_name="Значение восточной долготы на карте",
    )

    def __str__(self):
        return f"{self.latitude} - {self.longitude}"

    class Meta:
        verbose_name = "Геолокация"
        verbose_name_plural = "Геолокация городов РФ"
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"], name="unique_geo_city"
            )
        ]


class City(models.Model):
    """Данные городов с их координатами."""

    rus_name = models.CharField(
        "Город на русском языке", max_length=settings.DEFAULT_MAXLEN_CHARFIELD
    )
    geolocation = models.ForeignKey(
        GeolocationCity,
        on_delete=models.CASCADE,
        verbose_name="Геолокация города",
        help_text="Укажите геолокацию города",
    )

    def __str__(self):
        return f"{self.rus_name}"

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города РФ"
        constraints = [
            models.UniqueConstraint(
                fields=["rus_name", "geolocation"], name="unique_city"
            )
        ]


class Company(models.Model):
    """
    Класс для хранения информации о компаниях,
    которые могут производить ремонты автомобилей.
    """

    title = models.CharField(
        max_length=settings.DEFAULT_MAXLEN_CHARFIELD,
        unique=True,
        verbose_name="Название компании по ремонту",
        help_text="Укажите название компании",
    )
    description = models.TextField(
        null=True,
        verbose_name="Описание компании",
    )
    logo = models.ImageField(
        "Логотип компании",
        upload_to="autoservice/images/logo",
        null=True,
    )
    legal_address = models.CharField(
        null=True,
        max_length=250,
        verbose_name="Юридический адрес",
    )
    taxpayer_id = models.CharField(
        "ИНН юридического лица",
        max_length=10,
        null=False,
        validators=[validate_all_isdigit],
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Владелец компании",
        help_text="Укажите владельца компании",
        related_name="company",
        null=True,
    )

    class Meta:
        verbose_name = "Компания по ремонту авто"
        verbose_name_plural = "Компания по ремонту авто"

    def __str__(self):
        return f"{self.title}"


class GeolocationAutoService(models.Model):
    """
    Модель с геолокацией автосервисов.
    """

    latitude = models.FloatField(
        verbose_name="Значение северной широты на карте",
    )
    longitude = models.FloatField(
        verbose_name="Значение восточной долготы на карте",
    )

    def __str__(self):
        return f"{self.latitude} - {self.longitude}"

    class Meta:
        verbose_name = "геолокацию"
        verbose_name_plural = "Геолокация автосервисов РФ"
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"], name="unique_geo_service"
            )
        ]


class Job(models.Model):
    """Модель работ выполняемых автосервисами."""

    title = models.CharField(
        max_length=settings.MAX_LENGTH_JOBS_NAME,
        verbose_name="Название работы",
        unique=True,
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    def __str__(self):
        return self.title


class AutoService(models.Model):
    """Модель автосервиса."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        help_text="Выберите компанию",
    )
    address = models.CharField(
        max_length=250,
        verbose_name="Адрес автосервиса",
        help_text="Укажите адрес автосервиса",
    )
    geolocation = models.ForeignKey(
        GeolocationAutoService,
        on_delete=models.CASCADE,
        verbose_name="Геолокация автосервиса",
        help_text="Укажите геолокацию автосервиса",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город",
        help_text="Укажите город",
    )
    working_time = models.ManyToManyField(
        WorkingTime,
        blank=True,
        help_text="График работы автосервиса",
        related_name="autoservices",
    )
    phone_number = models.CharField(
        max_length=settings.PHONE_MAX_LENGTH,
        validators=[phone_number_validator],
        help_text="Введите номер телефона",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=settings.EMAIL_MAX_LENGTH,
        null=True,
        blank=True,
        help_text="Введите адрес электронной почты",
        validators=[ASCIIUsernameValidator()],
    )
    site = models.CharField(
        verbose_name="Сайт автосервиса",
        max_length=settings.EMAIL_MAX_LENGTH,
        null=True,
        blank=True,
        help_text=("Введите адрес сайта автосервиса в формате 'www.example.com'"),
    )
    job = models.ManyToManyField(
        Job,
        blank=True,
        through="AutoserviceJob",
        verbose_name="Работы",
        help_text="Выберите необходимый тип работ",
    )
    car_service = models.ManyToManyField(
        Transport,
        blank=True,
        related_name="autoservices",
        verbose_name="Автомобильные бренды",
        help_text="Выберите автомобильные бренды",
    )

    class Meta:
        verbose_name = "Автосервис"
        verbose_name_plural = "Автосервисы"

    def __str__(self):
        return f"{self.company.title} - {self.geolocation}"


class AutoserviceJob(models.Model):
    """Модель для связи модели автосервиса и модели работы."""

    service = models.ForeignKey(
        AutoService,
        on_delete=models.CASCADE,
        verbose_name="Автосервис",
        help_text="Выберите автосервис",
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        verbose_name="Тип работы автосервиса",
        help_text="Выберите необходимый тип работ",
    )
    price = models.FloatField(
        verbose_name="Стоимость работ",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, message="Стоимость ниже 1 невозможна"),
        ],
    )

    def __str__(self) -> str:
        return f"{self.job.title} — {self.price}"

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы и прайсы автосервисов"
        constraints = [
            models.UniqueConstraint(
                fields=["service", "job"], name="unique_service_job"
            )
        ]


class Feedback(models.Model):
    """
    Класс Feedback представляет модель отзыва на автосервис,
    который может быть оставлен пользователем.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback",
        verbose_name="Автор отзыва",
    )
    autoservice = models.ForeignKey(
        AutoService,
        on_delete=models.CASCADE,
        related_name="feedback",
        verbose_name="Автосервис, на который пользователь пишет отзыв",
    )
    text = models.TextField(
        verbose_name="Текст отзыва", help_text="Напишите ваш отзыв тут"
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Оценка ниже 1 невозможна"),
            MaxValueValidator(5, message="Оценка выше 5 невозможна"),
        ],
        verbose_name="Оценка автосервиса от пользователя",
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "autoservice"], name="unique_feedback"
            )
        ]

    def __str__(self) -> str:
        return f"{self.text[:25]}"


class Image(models.Model):
    # Путь, куда будут загружаться изображения
    image = models.ImageField(upload_to="feedback/images/")
    # Связь с моделью Feedback
    feedbacks = models.ManyToManyField(Feedback, related_name="images")
