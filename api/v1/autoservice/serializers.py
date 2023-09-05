from autoservice.models import Company, AutoService
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class AutoServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoService
        fields = '__all__'


class AutoServiceFromGeoSerializer(serializers.ModelSerializer):

    geo_size = serializers.SerializerMethodField()

    class Meta:
        model = AutoService
        fields = [

        ]

    def get_geo_size(self, obj):
        return 1
