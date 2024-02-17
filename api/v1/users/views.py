from typing import Callable
from django.shortcuts import redirect
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
import requests
from rest_framework.decorators import action, permission_classes
from api.v1.autoservice.serializers import CompanyRegistrationSerializer

from api.v1.users.exceptions import InvalidRegistrationMethodException

from .serializers import CompanyOwnerSerializer, CustomUserSerializer


@extend_schema(
    tags=["Пользователь"],
    methods=["POST", "GET", "PATCH", "DELETE", "PUT"],
    #  description="API для управления списком заказов."
)
@extend_schema_view(
    create=extend_schema(
        tags=["Пользователь"],
        description="Создание пользователя",
        summary="Создание пользователя",
    ),
    list=extend_schema(
        tags=["Пользователь"],
        description="Получение списка пользователей",
        summary="Получение списка пользователей",
    ),
    retrieve=extend_schema(
        tags=["Пользователь"],
        description="Получение информации о пользователе",
        summary="Получение информации о пользователе",
    ),
    update=extend_schema(
        tags=["Пользователь"],
        description="Обновление информации о пользователе",
        summary="Обновление информации о пользователе",
    ),
    partial_update=extend_schema(
        tags=["Пользователь"],
        description="Частичное обновление информации о пользователе",
        summary="Частичное обновление информации о пользователе",
    ),
    destroy=extend_schema(
        tags=["Пользователь"],
        description="Удаление пользователя",
        summary="Удаление пользователя",
    ),
    activation=extend_schema(
        tags=["Пользователь"],
        description="Активация пользователя по uid и token",
        summary="Активация пользователя",
    ),
    me=[
        extend_schema(
            tags=["Пользователь"],
            description="Получение информации о текущем пользователе",
            summary="Получение информации о текущем пользователе",
            methods=["GET"],
        ),
        extend_schema(
            tags=["Пользователь"],
            description="Изменение информации о текущем пользователе",
            summary="Изменение информации о текущем пользователе",
            methods=["PUT"],
        ),
        extend_schema(
            tags=["Пользователь"],
            description="Частичное обновление информации о текущем пользователе",
            summary="Частичное обновление информации о текущем пользователе",
            methods=["PATCH"],
        ),
        extend_schema(
            tags=["Пользователь"],
            description="Удаление текущего пользователя",
            summary="Удаление текущего пользователя",
            methods=["DELETE"],
        ),
    ],
    resend_activation=extend_schema(
        tags=["Пользователь"],
        description="Запрос на повторное отправление кода активации",
        summary="Повторная отправка кода активации",
    ),
    reset_password=extend_schema(
        tags=["Пользователь"],
        description="Запрос на сброс пароля пользователя",
        summary="Сброс пароля пользователя",
    ),
    reset_password_confirm=extend_schema(
        tags=["Пользователь"],
        description="Подтверждение сброса пароля пользователя",
        summary=" Подтверждение сброса пароля",
    ),
    reset_username=extend_schema(
        tags=["Пользователь"],
        description="Запрос на смену имени пользователя",
        summary="Смена имени пользователя",
    ),
    reset_username_confirm=extend_schema(
        tags=["Пользователь"],
        description="Подтверждение смены имени пользователя",
        summary="Подтверждение смены имени пользователя",
    ),
    set_password=extend_schema(
        tags=["Пользователь"],
        description="Установка нового пароля пользователя",
        summary="Установка нового пароля",
    ),
    set_username=extend_schema(
        tags=["Пользователь"],
        description="Установка нового имени пользователя.",
        summary="Установка нового имени пользователя",
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
        try:
            registration_method = self.get_registration_method(request)
            return registration_method(request, *args, **kwargs)
        except InvalidRegistrationMethodException:
            return Response(
                {"error": "Invalid registration method"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_registration_method(self, request, *args, **kwargs) -> Callable:
        registration_by_phone = request.data.get("phone_number", None)
        registration_by_email = request.data.get("email", None)

        if registration_by_email:
            return super().create
        else:
            raise InvalidRegistrationMethodException

    @extend_schema(
        description="Регистрирует пользователя в качестве владельца автосервиса. \
                     Создает компанию юрлицо владельца автосервиса.",
        parameters=[
            CompanyOwnerSerializer,
        ],
        request=CompanyOwnerSerializer,
        responses={201: CompanyOwnerSerializer, 400: None},
        methods=["POST"],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create-companyowner",
        url_name="create_companyowner",
        permission_classes=[],
    )
    def create_companyowner(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data.get("owner"))
        user_serializer.is_valid(raise_exception=True)
        self.perform_create(user_serializer)

        owner = user_serializer.instance
        if isinstance(user_serializer, CustomUserSerializer):
            user_serializer.add_company_owners_group(owner)
        else:
            print(f"can't company_owners_group to {owner} of type {type(owner)}")
            print(f"user {owner} of type {type(owner)} is created")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        company_serializer = CompanyRegistrationSerializer(
            data=request.data.get("company")
        )
        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()
        company.owner = owner
        company.save()

        data = {"owner": user_serializer.data, "company": company_serializer.data}

        headers = self.get_success_headers(company_serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    tags=["Пользователь"],
    methods=["GET", "POST", "DELETE"],
)
@extend_schema_view(
    get=extend_schema(
        tags=["Пользователь"],
        description="""Эндпоинт используется для активации пользователя.
                                    При переходе по этой ссылке пользователь будет автоматически активирован передайте
                                    uid и token""",
        summary="Активация пользователя",
    ),
)
class CustomUserActivation(APIView):
    """Вью-функция предназначена для автоматизации активации пользователя при
    переходе по ссылке для подтверждения почты путем передачи параметров
    GET-запроса в теле POST-запроса на стандартный url Djoser.
    """

    def get(self, request, uid, token):
        data = {"uid": uid, "token": token}
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/users/activation/", json=data
        )

        if response.status_code == 204:
            return Response(
                {"message": "User activation successful"}, status=200
            )
        elif response.status_code == 200:
            try:
                response_data = response.json()
                return Response(response_data)
            except ValueError:
                return Response(
                    {"error": "Invalid JSON response from the server"},
                    status=500,
                )
        else:
            return Response(
                {
                    "error": f"Request failed with status code {response.status_code}"
                },
                status=response.status_code,
            )
