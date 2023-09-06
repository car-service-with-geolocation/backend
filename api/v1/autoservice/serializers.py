from autoservice.models import Company, AutoService
from rest_framework import serializers
from core.utils import calc_autoservice_distance_for_user


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class AutoServiceSerializer(serializers.ModelSerializer):

    company = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Company.objects.all()
    )
    geo_size = serializers.SerializerMethodField()

    class Meta:
        model = AutoService
        fields = [
            'company',
            'latitude',
            'longitude',
            'address',
            'geo_size',
        ]

    def get_geo_size(self, obj):
        la = float(self.context['request'].query_params['latitude'])
        lo = float(self.context['request'].query_params['longitude'])
        return calc_autoservice_distance_for_user(
            la, obj.latitude, lo, obj.longitude
        )
