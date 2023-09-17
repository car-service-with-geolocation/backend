from django.shortcuts import get_object_or_404

from rest_framework import serializers

from autoservice.models import (
    AutoService,
    Company,
    City,
    GeolocationAutoService,
)
from feedback.models import Feedback
from core.utils import calc_autoservice_distance_for_user


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для компаний автосервисов.
    """
    class Meta:
        model = Company
        fields = ['name', 'description', 'logo', 'slug', 'legal_address']


class GeolocationAutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для геолокации автосервиса.
    """
    class Meta:
        model = GeolocationAutoService
        fields = ['latitude', 'longitude']


class AutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка автосервисов.
    """
    company = CompanySerializer()
    geolocation = GeolocationAutoServiceSerializer()
    city = serializers.SlugRelatedField(
        queryset=City.objects.all(),
        slug_field='rus_name',
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = AutoService
        fields = [
            'company',
            'city',
            'address',
            'geolocation',
            'rating',
        ]

    def get_rating(self, obj):
        return 0


class GetServiceFromUserSerializer(serializers.Serializer):
    usr_lat = serializers.FloatField(write_only=True)
    usr_long = serializers.FloatField(write_only=True)

    def to_representation(self, instance):
        request = self.context.get('request')
        return AutoServiceSerializer(
            AutoService.objects.all(),
            instance,
            context={'request': request}
        ).data

class AutoServiceGeoIPSerializer(serializers.ModelSerializer):
    """
    Сериализатор для автосервисов с геолокацией.
    Имеет присебе расчет расстояния до каждого
    автосервиса от текущего положения клиента.
    """
    company = CompanySerializer()
    geolocation = GeolocationAutoServiceSerializer()
    city = serializers.SlugRelatedField(
        slug_field='rus_name',
        queryset=City.objects.all()
    )
    geo_size = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = AutoService
        fields = [
            'company',
            'city',
            'address',
            'geolocation',
            'geo_size',
            'rating',
        ]

    def get_rating(self, obj):
        return 0

    def get_geo_size(self, obj):
        """
        Расчет растояния от клиента до сервиса.
        """
        la = float(self.context['request'].query_params['latitude'])
        lo = float(self.context['request'].query_params['longitude'])
        return calc_autoservice_distance_for_user(
            la, obj.geolocation.latitude, lo, obj.geolocation.longitude
        )


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
