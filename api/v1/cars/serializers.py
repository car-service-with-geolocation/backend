from rest_framework import serializers

from cars.models import Cars, Transport


class TransportsSerializer(serializers.ModelSerializer):
    """Сериализатор для списка брендов/моделей автомобилей"""
    class Meta:
        model = Transport
        fields = ('id', 'brand', 'slug')


class CarsSerializer(serializers.ModelSerializer):
    """Сериализатор для информации об автомобиле"""
    car = TransportsSerializer()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Cars
        fields = ('id', 'owner', 'car', 'color', 'vin',
                  'number_of_car', 'odometr', 'year', 'last_service_date')
