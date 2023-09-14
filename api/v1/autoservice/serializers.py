from django.shortcuts import get_object_or_404

from rest_framework import serializers

from autoservice.models import Company, AutoService
from feedback.models import Feedback
from core.utils import calc_autoservice_distance_for_user


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для компаний автосервисов.
    """
    class Meta:
        model = Company
        fields = '__all__'


class AutoServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для автосервисов.
    """
    company = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Company.objects.all()
    )
    rating = serializers.IntegerField()

    class Meta:
        model = AutoService
        fields = [
            'company',
            'latitude',
            'longitude',
            'address',
            'rating',
        ]


class AutoServiceGeoIPSerializer(serializers.ModelSerializer):
    """
    Сериализатор для автосервисов с геолокацией.
    Имеет присебе расчет расстояния до каждого
    автосервиса от текущего положения клиента.
    """
    company = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Company.objects.all()
    )
    geo_size = serializers.SerializerMethodField()
    rating = serializers.IntegerField()

    class Meta:
        model = AutoService
        fields = [
            'company',
            'latitude',
            'longitude',
            'address',
            'geo_size',
            'city',
            'rating',
        ]

    def get_geo_size(self, obj):
        """
        Расчет растояния от клиента до сервиса.
        """
        la = float(self.context['request'].query_params['latitude'])
        lo = float(self.context['request'].query_params['longitude'])
        return calc_autoservice_distance_for_user(
            la, obj.latitude, lo, obj.longitude
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
