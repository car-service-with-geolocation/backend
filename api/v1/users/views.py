from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет предоставляет весь функционал CRUD для модели CustomUser
    Вьюсет наследует стандартный UserViewSet из Djoser с последующим
    переопределением метода create для регистрации пользователей по номеру
    телефона.
    """
    serializer = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        registration_by_phone = request.data.get('phone_number', None)
        registration_by_email = request.data.get('email', None)

        if registration_by_phone:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        if registration_by_email:
            return super().create(request, *args, **kwargs)

        return Response({'error': 'Invalid registration method'},
                        status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
        # TO DO


class CustomUserActivation(APIView):
    """
    Вью-функция предназначена для автоматизации активации пользователя при
    переходе по ссылке для подтверждения почты путем передачи параметров
    GET-запроса в теле POST-запроса на стандартный url Djoser
    """
    def get(self, request, uid, token):
        data = {
            "uid": uid,
            "token": token
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/users/activation/",
            data=data
        )
        return Response(status=response.status_code)
