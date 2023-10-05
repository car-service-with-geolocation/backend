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
                  'username',
                  'password',
                  'last_name',
                  'first_name',
                  'phone_number',
                  'date_joined',
                  'image'
                  )
