from django.shortcuts import get_object_or_404

from rest_framework import serializers

from autoservice.models import (
    AutoService,
    Company,
    City,
    GeolocationAutoService,
    AutoserviceJob,
)
from api.v1.cars.serializers import TransportsSerializer
from feedback.models import Feedback
from core.utils import calc_autoservice_distance_for_user


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


class AutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка автосервисов.
    """
    company = CompanySerializer()
    geolocation = GeolocationAutoServiceSerializer()
    city = serializers.SlugRelatedField(
        slug_field='rus_name',
        queryset=City.objects.all()
    )
    car_service = TransportsSerializer(many=True)
    job = serializers.SerializerMethodField()

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
            'openfrom',
            'openuntil',
            'holidays',
            'phone_number',
            'email',
            'site',
            'car_service',
            'job',
        ]

    def get_job(self, obj):
        job = AutoserviceJob.objects.filter(service=obj)
        return AutoserviceJobSerializer(job, many=True).data


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Feedback."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
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
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'score',
        )
        model = Feedback
