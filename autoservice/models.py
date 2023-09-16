from django.db import models
    

class GeolocationCity(models.Model):
    """
    Модель с геолокацией городов.
    """
    latitude = models.FloatField(
        verbose_name="Значение северной широты на карте",
    )
    longitude = models.FloatField(
        verbose_name="Значение восточной долготы на карте",
    )

    def __str__(self):
        return f"{self.latitude} - {self.longitude}"


class City(models.Model):
    """Данные городов с их координатами."""
    rus_name = models.CharField(
        'Город на русском языке',
        max_length=255
    )
    geolocation = models.ForeignKey(
        GeolocationCity,
        on_delete=models.CASCADE,
        verbose_name="Геолокация города",
        help_text="Укажите геолокацию города"
    )

    def __str__(self):
        return f"{self.rus_name}"


class Company(models.Model):
    """
    Класс для хранения информации о компаниях,
    которые могут производить ремонты автомобилей.
    """
    name = models.CharField(
        max_length=250,
        verbose_name="Название компании по ремонту",
        help_text="Укажите название компании"
    )
    description = models.TextField(
        verbose_name="Описание компании",
    )
    logo = models.ImageField(
        'Логотип компании', 
        upload_to='logo_companys/',
        null=True,
    )
    slug = models.SlugField()
    legal_address = models.CharField(
        max_length=250,
        verbose_name="Юридический адрес",
    )

    class Meta:
        verbose_name = "Компания по ремонту авто"
        verbose_name_plural = "Компания по ремонту авто"

    def __str__(self):
        return f"{self.name}"
    

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


class AutoService(models.Model):
    """
    Модель для хранения данных об автосервисах.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        help_text="Выберите компанию"
    )
    address = models.CharField(
        max_length=250,
        verbose_name="Адрес автосервиса",
        help_text="Укажите адрес автосервиса"
    )
    geolocation = models.ForeignKey(
        GeolocationAutoService,
        on_delete=models.CASCADE,
        verbose_name="Геолокация автосервиса",
        help_text="Укажите геолокацию автосервиса"
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='Город',
        help_text='Укажите город'
    )

    class Meta:
        verbose_name = "Автосервис"
        verbose_name_plural = "Автосервис"

    def __str__(self):
        return (
            f"{self.company.name} - "
            f"{self.geolocation}"
        )
