from rest_framework import serializers

from autoservice.models import Job


class JobsSerializer(serializers.ModelSerializer):
    """Сериализатор для работ автосервиса"""
    class Meta:
        model = Job
        fields = "__all__"
