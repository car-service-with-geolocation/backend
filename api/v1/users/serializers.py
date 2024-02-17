from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from djoser.serializers import UserSerializer
from rest_framework import serializers
from api.v1.autoservice.serializers import CompanyRegistrationSerializer

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
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)

    def add_company_owners_group(self, instance):
        group, _ = Group.objects.get_or_create(name='company_owners')
        instance.groups.add(group)
        instance.save()


class CustomCurrentUserSerializer(UserSerializer):
    """
    Сериализатор для модели пользователя CustomUser.
    Когда пользователь аутентифицирован.
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

    def update(self, instance, validated_data):
        if validated_data.get('password', None) is not None:
            validated_data['password'] = make_password(
                validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class CompanyOwnerSerializer(serializers.Serializer):
    owner = CustomUserSerializer()
    company = CompanyRegistrationSerializer()
