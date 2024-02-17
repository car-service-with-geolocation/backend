import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from autoservice.models import (
    AutoService,
    AutoserviceJob,
    City,
    Company,
    Feedback,
    GeolocationAutoService,
    Image,
    Job,
    Transport,
    WorkingTime,
)


class TransportsSerializer(serializers.ModelSerializer):
    """Сериализатор для списка брендов (моделей) автомобилей."""

    class Meta:
        model = Transport
        fields = ("id", "brand")


class CompanySerializer(serializers.ModelSerializer):
    """Сериализатор для компаний автосервисов."""

    class Meta:
        model = Company
        fields = [
            "id",
            "title",
            "description",
            "logo",
            "legal_address",
            "owner",
        ]


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации компаний автосервисов."""

    class Meta:
        model = Company
        fields = [
            "title",
            "legal_address",
            "taxpayer_id",
        ]

class CompanyShortSerializer(serializers.ModelSerializer):
    """Сериализатор для компаний автосервисов
    (Необходим для списка автосервисов).
    """

    class Meta:
        model = Company
        fields = ["title", "logo"]


class GeolocationAutoServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для геолокации автосервиса."""

    class Meta:
        model = GeolocationAutoService
        fields = ["latitude", "longitude"]


class AutoserviceJobSerializer(serializers.ModelSerializer):
    """Сериализатор для работ автосервисов и их прайс."""

    id = serializers.IntegerField(source="job.id", read_only=True)
    title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = AutoserviceJob
        fields = [
            "id",
            "title",
            "price",
        ]


class WorkTimeSerializer(serializers.ModelSerializer):
    """Сериализатор для графиков работ автосервисов."""

    class Meta:
        model = WorkingTime
        fields = [
            "id",
            "day",
            "time",
        ]


class ListAutoServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для списка автосервисов."""

    company = CompanyShortSerializer()
    geolocation = GeolocationAutoServiceSerializer()
    rating = serializers.FloatField(read_only=True)
    votes = serializers.IntegerField(read_only=True)
    working_time_today = serializers.SerializerMethodField()

    class Meta:
        model = AutoService
        fields = [
            "id",
            "company",
            "geolocation",
            "address",
            "rating",
            "votes",
            "working_time_today",
        ]

    def get_working_time_today(self, obj: AutoService) -> str:
        """
        Функция возвращает график работы автосервиса в определенный (текущий)
        день недели (сегодня).
        Принимает экземпляр автосервиса в качестве аргумента и выводит
        'сегодняшний' график работы этого автосервиса.
        Параметры:
        obj (AutoService): Экземпляр автосервиса, на который нужно вывести
        график работы на 'сегодня'.
        Возвращает:
        str: График работы автосервиса (сегодня).
        """
        current_time = datetime.datetime.now()
        number_day_of_week = current_time.weekday()
        working_days_in_current_autoservices = obj.working_time.all()
        for item in working_days_in_current_autoservices:
            if item.day == settings.NUMBER_WEEK[number_day_of_week]:
                return f"{item.day}: {item.time}"


class AutoServiceSerializer(serializers.ModelSerializer):
    """Сериализатор автосервиса."""

    company = CompanySerializer()
    geolocation = GeolocationAutoServiceSerializer()
    city = serializers.SlugRelatedField(
        slug_field="rus_name", queryset=City.objects.all()
    )
    car_service = TransportsSerializer(many=True)
    working_time = WorkTimeSerializer(many=True)
    job = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = AutoService
        fields = [
            "id",
            "company",
            "geolocation",
            "city",
            "address",
            "rating",
            "votes",
            "working_time",
            "phone_number",
            "email",
            "site",
            "car_service",
            "job",
        ]

    def get_job(self, obj):
        job = AutoserviceJob.objects.filter(service=obj)
        return AutoserviceJobSerializer(job, many=True).data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Feedback."""

    # поле для изображений
    images = ImageSerializer(
        many=True, required=False, help_text="Загрузите изображение (необязательно)"
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="email", default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        if Feedback.objects.filter(
            author=self.context["request"].user,
            autoservice=get_object_or_404(
                AutoService, id=self.context["view"].kwargs.get("autoservice_id")
            ),
        ).exists():
            raise serializers.ValidationError("Можно оставить только один отзыв")
        return data

    class Meta:
        model = Feedback
        fields = (
            "id",
            "author",
            "text",
            "score",
            "pub_date",
            "images",
        )


class JobsSerializer(serializers.ModelSerializer):
    """Сериализатор для работ автосервиса."""

    class Meta:
        model = Job
        fields = "__all__"
