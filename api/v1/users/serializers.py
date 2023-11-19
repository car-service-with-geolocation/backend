from django.contrib.auth.hashers import make_password
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для модели пользователя CustomUser
    """
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'first_name',
                  'password',
                  'phone_number',
                  'date_joined'
                  )

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
