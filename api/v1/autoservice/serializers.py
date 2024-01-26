from django.shortcuts import get_object_or_404
from rest_framework import serializers

from autoservice.models import (
    AutoService,
    AutoserviceJob,
    City,
    Company,
    Feedback,
    GeolocationAutoService,
    Job,
    Transport,
    WorkTimeRange,
    WorkingTime, Image,
)


class TransportsSerializer(serializers.ModelSerializer):
    """Сериализатор для списка брендов/моделей автомобилей"""
    class Meta:
        model = Transport
        fields = ('id', 'brand')


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для компаний автосервисов.
    """
    class Meta:
        model = Company
        fields = [
            'id',
            'title',
            'description',
            'logo',
            'legal_address',
        ]


class CompanyShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для компаний автосервисов (с укороченным набором полей).
    """
    class Meta:
        model = Company
        fields = [
            'id',
            'title',
            'logo',
        ]


class GeolocationAutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для геолокации автосервиса.
    """
    class Meta:
        model = GeolocationAutoService
        fields = ['latitude', 'longitude']


class AutoserviceJobSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работ автосервисов и их прайс.
    """
    id = serializers.IntegerField(source='job.id', read_only=True)
    title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = AutoserviceJob
        fields = [
            'id',
            'title',
            'price',
        ]


class WorkTimeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkTimeRange
        fields = [
            'openfrom',
            'openuntil',
        ]


class WorkTimeSerializer(serializers.ModelSerializer):

    monday = WorkTimeRangeSerializer()
    tuesday = WorkTimeRangeSerializer()
    wednesday = WorkTimeRangeSerializer()
    thursday = WorkTimeRangeSerializer()
    friday = WorkTimeRangeSerializer()
    saturday = WorkTimeRangeSerializer()
    sunday = WorkTimeRangeSerializer()

    class Meta:
        model = WorkingTime
        fields = [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
        ]


class ListAutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка автосервисов.
    """
    company = CompanyShortSerializer()
    geolocation = GeolocationAutoServiceSerializer()
    rating = serializers.FloatField(read_only=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = AutoService
        fields = [
            'id',
            'company',
            'geolocation',
            'address',
            'rating',
            'votes',
            'working_time_text',
        ]


class AutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор автосервиса.
    """
    company = CompanySerializer()
    geolocation = GeolocationAutoServiceSerializer()
    city = serializers.SlugRelatedField(
        slug_field='rus_name',
        queryset=City.objects.all()
    )
    car_service = TransportsSerializer(many=True)
    working_time = WorkTimeSerializer()
    job = serializers.SerializerMethodField()

    rating = serializers.FloatField(read_only=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = AutoService
        fields = [
            'id',
            'company',
            'geolocation',
            'city',
            'address',
            'rating',
            'votes',
            'working_time_text',
            'working_time',
            'phone_number',
            'email',
            'site',
            'car_service',
            'job',
        ]

    def get_job(self, obj):
        job = AutoserviceJob.objects.filter(service=obj)
        return AutoserviceJobSerializer(job, many=True).data


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'image']


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Feedback.
    """
    # поле для изображений
    images = ImageSerializer(
        many=True,
        required=False,
        help_text='Загрузите изображение (необязательно)'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Feedback.objects.filter(
            author=self.context['request'].user,
            autoservice=get_object_or_404(
                AutoService,
                id=self.context['view'].kwargs.get('autoservice_id')
            )
        ).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв'
            )
        return data

    class Meta:
        model = Feedback
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date',
            'images',
        )


class JobsSerializer(serializers.ModelSerializer):
    """Сериализатор для работ автосервиса"""

    class Meta:
        model = Job
        fields = "__all__"
