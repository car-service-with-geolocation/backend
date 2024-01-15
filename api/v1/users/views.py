from django.shortcuts import redirect
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .serializers import CustomUserSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    tags = ["Пользователь"],
    methods = ["POST", "GET", "PATCH", "DELETE", "PUT"],
  #  description="API для управления списком заказов."
)
@extend_schema_view(
    create = extend_schema(tags = ["Пользователь"],
                         description = "Создание пользователя",
                         summary = "Создание пользователя"),
    list = extend_schema(tags = ["Пользователь"],
                       description = "Получение списка пользователей",
                       summary = "Получение списка пользователей"),
    retrieve = extend_schema(tags = ["Пользователь"],
                           description = "Получение информации о пользователе",
                           summary = "Получение информации о пользователе"),
    update = extend_schema(tags = ["Пользователь"],
                         description = "Обновление информации о пользователе",
                         summary = "Обновление информации о пользователе"),
    partial_update = extend_schema(tags = ["Пользователь"],
                                 description = "Частичное обновление информации о пользователе",
                                 summary = "Частичное обновление информации о пользователе"),
    destroy = extend_schema(tags = ["Пользователь"],
                          description = "Удаление пользователя",
                          summary = "Удаление пользователя"),
    activation = extend_schema(tags = ["Пользователь"],
                          description = "Активация пользователя по uid и token",
                          summary = "Активация пользователя"),
    me = [
        extend_schema(
            tags = ["Пользователь"],
            description = "Получение информации о текущем пользователе",
            summary = "Получение информации о текущем пользователе",
            methods = ["GET"],
        ),
        extend_schema(
            tags = ["Пользователь"],
            description = "Изменение информации о текущем пользователе",
            summary = "Изменение информации о текущем пользователе",
            methods = ["PUT"],
        ),
        extend_schema(
            tags = ["Пользователь"],
            description = "Частичное обновление информации о текущем пользователе",
            summary = "Частичное обновление информации о текущем пользователе",
            methods = ["PATCH"],
        ),
        extend_schema(
            tags = ["Пользователь"],
            description = "Удаление текущего пользователя",
            summary = "Удаление текущего пользователя",
            methods = ["DELETE"],
        ),
    ],
    resend_activation = extend_schema(
            tags = ["Пользователь"],
            description = "Запрос на повторное отправление кода активации",
            summary = "Повторная отправка кода активации",
        ),
    reset_password = extend_schema(
            tags = ["Пользователь"],
            description = "Запрос на сброс пароля пользователя",
            summary = "Сброс пароля пользователя",
        ),
    reset_password_confirm = extend_schema(
            tags = ["Пользователь"],
            description = "Подтверждение сброса пароля пользователя",
            summary = " Подтверждение сброса пароля",
        ),
    reset_username = extend_schema(
            tags = ["Пользователь"],
            description = "Запрос на смену имени пользователя",
            summary = "Смена имени пользователя",
        ),
    reset_username_confirm = extend_schema(
            tags = ["Пользователь"],
            description = "Подтверждение смены имени пользователя",
            summary = "Подтверждение смены имени пользователя",
        ),
    set_password = extend_schema(
            tags = ["Пользователь"],
            description = "Установка нового пароля пользователя",
            summary = "Установка нового пароля",
        ),
    set_username = extend_schema(
            tags = ["Пользователь"],
            description = "Установка нового имени пользователя.",
            summary = "Установка нового имени пользователя",
        ),

)
class CustomUserViewSet(UserViewSet):
    """
    Вьюсет предоставляет весь функционал CRUD для модели CustomUser
    Вьюсет наследует стандартный UserViewSet из Djoser с последующим
    переопределением метода create для регистрации пользователей по номеру
    телефона.
    """

    def create(self, request, *args, **kwargs):
        registration_by_phone = request.data.get("phone_number", None)
        registration_by_email = request.data.get("email", None)

        if registration_by_email:
            return super().create(request, *args, **kwargs)

        return Response(
            {"error": "Invalid registration method"}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=["Пользователь"],
    methods=["GET", "POST", "DELETE"],
)
@extend_schema_view(
    get=extend_schema(tags=["Пользователь"],
                      description='''Эндпоинт используется для активации пользователя.
                                    При переходе по этой ссылке пользователь будет автоматически активирован передайте
                                    uid и token''',
                      summary="Активация пользователя"),
)
class CustomUserActivation(APIView):

    # Вью-функция предназначена для автоматизации активации пользователя при
    # переходе по ссылке для подтверждения почты путем передачи параметров
    # GET-запроса в теле POST-запроса на стандартный url Djoser

    def get(self, request, uid, token):
        data = {
            "uid": uid,
            "token": token
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/users/activation/",
            data=data
        )
        return redirect('/')
