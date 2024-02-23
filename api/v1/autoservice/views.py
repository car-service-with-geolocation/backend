from copy import copy
from django.contrib.auth.models import Group
from django.db.models import Avg, Count, F
from django.db.models.functions import ASin, Cos, Power, Radians, Sin, Sqrt
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.v1.users.serializers import CustomUserSerializer

from api.v1.users.views import CustomUserViewSet
from autoservice.models import AutoService, Company, Image, Job, Transport
from core.utils import is_float
from users.models import CustomUser

from .filters import JobsFilter, TransportsFilter
from .permissions import IsAuthorOrAdminReadOnly
from .serializers import (
    AutoServiceSerializer,
    CompanySerializer,
    FeedbackSerializer,
    JobsSerializer,
    ListAutoServiceSerializer,
    TransportsSerializer,
)


@extend_schema(
    tags=["Автосервисы"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(
        description="Получить список всех моделей автомобилей",
        summary="Получить список моделей а/м ",
    )
)
class TransportList(generics.ListAPIView):
    """ListAPIView для чтения информации о компаниях по ремонту авто."""

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TransportsFilter
    search_fields = ("brand",)


@extend_schema(
    tags=["Автосервисы"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(
        description="Получить информацию о модели автомобиля по id",
        summary="Получить информацию а/м по id",
    )
)
class TransportDetail(generics.RetrieveAPIView):
    """APIView для чтения информации о компаниях по ремонту авто."""

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer


@extend_schema(
    tags=["Автосервисы"],
    methods=["GET"],
)
@extend_schema_view(
    list=extend_schema(
        description="Получить список компаний по ремонту авто",
        summary="Получить список компаний",
        tags=["Автосервисы"],
    ),
    retrieve=extend_schema(
        description="Получить информацию о компании по ремонту авто",
        summary="Получить информация о компании по id",
        tags=["Автосервисы"],
    ),
)
class CompanyViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@extend_schema(
    tags=["Автосервисы"],
    methods=["GET"],
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список автосервисов.",
        description="Получить список автосервисов , param: latitude",
        tags=["Автосервисы"],
    ),
    retrieve=extend_schema(
        summary="Получить детали автосервиса по id",
        description="Получить детали автосервиса по id",
        tags=["Автосервисы"],
    ),
)
class AutoServiceViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """ViewSet для получения списка автосервисов.
    param: latitude.
    """

    serializer_class = AutoServiceSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in "list":
            return ListAutoServiceSerializer
        return AutoServiceSerializer

    def get_queryset(self):
        queryset = (
            AutoService.objects.select_related("geolocation")
            .annotate(rating=Avg("feedback__score"), votes=Count("feedback__score"))
            .order_by("-rating")
        )
        if (
            "latitude" in self.request.query_params
            and "longitude" in self.request.query_params
            and is_float(self.request.query_params["latitude"])
            and is_float(self.request.query_params["longitude"])
        ):
            lat = float(self.request.query_params["latitude"])
            lon = float(self.request.query_params["longitude"])
            # todo Вынести логику подсчета в отдельную функцию, убрать ее из views.py
            queryset = queryset.annotate(
                distance=(
                    2
                    * 6371
                    * ASin(
                        Sqrt(
                            Power(
                                Sin(
                                    (Radians(F("geolocation__latitude")) - Radians(lat))
                                    / 2
                                ),
                                2,
                            )
                            + Cos(Radians(lat))
                            * Cos(Radians(F("geolocation__latitude")))
                            * Power(
                                Sin(
                                    (
                                        Radians(F("geolocation__longitude"))
                                        - Radians(lon)
                                    )
                                    / 2
                                ),
                                2,
                            )
                        )
                    )
                )
            ).order_by("distance", "-rating")
        return queryset


@extend_schema(
    tags=["Отзывы"],
    methods=["GET", "POST", "PATCH", "DELETE"],
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить отзывы об автосервисе",
        description="Получить список отзывыв об автосервисе необходимо указать id автосервиса",
        tags=["Отзывы"],
    ),
    create=extend_schema(
        summary="Создать отзыв об автосервисе",
        description="Создать отзыв об автосервисе необходимо указать id автосервиса",
        tags=["Отзывы"],
    ),
    retrieve=extend_schema(
        summary="Получить детали отзыва об автосервисе",
        description="Получить детали отзыва об автосервисе необходимо указать id автосервиса и id отзыва",
        tags=["Отзывы"],
    ),
    update=extend_schema(
        summary="Изменить отзыв об автосервисе ",
        description="Изменить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags=["Отзывы"],
    ),
    partial_update=extend_schema(
        summary="Изменить отзыв об автосервисе.",
        description="Изменить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags=["Отзывы"],
    ),
    destroy=extend_schema(
        summary="Удалить отзыв об автосервисе",
        description="Удалить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags=["Отзывы"],
    ),
)
class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet для модели отзывов Feedback."""

    serializer_class = FeedbackSerializer
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = [IsAuthorOrAdminReadOnly]

    def get_autoservice(self):
        return get_object_or_404(AutoService, pk=self.kwargs.get("autoservice_id"))

    def get_queryset(self):
        return self.get_autoservice().feedback.all()

    def perform_create(self, serializer):
        feedback = serializer.save(
            author=self.request.user, autoservice=self.get_autoservice()
        )

        for file in self.request.FILES.getlist("images"):
            image = Image.objects.create(image=file)
            feedback.images.add(image)


@extend_schema(
    tags=["Работы"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(
        description="Получить список всех работ", summary="Получить все данные"
    )
)
class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = JobsFilter
    search_fields = ("name",)


@extend_schema(
    tags=["Работы"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(
        description="Получить подробную информацию о конкретной работе",
        summary="Получить данные по id",
    )
)
class JobsDetail(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer


@extend_schema(
    tags=["Владелец компании"],
    methods=["POST", "GET", "PATCH", "DELETE", "PUT"],
    description="Управление компанией как её владелец"
)
@extend_schema_view(
    create=extend_schema(
        tags=["Владелец компании"],
        description="Создание пользователя",
        summary="Создание пользователя",
    ),
    list=extend_schema(
        tags=["Владелец компании"],
        description="Получение списка пользователей",
        summary="Получение списка пользователей",
    ),
    retrieve=extend_schema(
        tags=["Владелец компании"],
        description="Получение информации о пользователе",
        summary="Получение информации о пользователе",
    ),
    update=extend_schema(
        tags=["Владелец компании"],
        description="Обновление информации о пользователе",
        summary="Обновление информации о пользователе",
    ),
    partial_update=extend_schema(
        tags=["Владелец компании"],
        description="Частичное обновление информации о пользователе",
        summary="Частичное обновление информации о пользователе",
    ),
    destroy=extend_schema(
        tags=["Владелец компании"],
        description="Удаление пользователя",
        summary="Удаление пользователя",
    ),
    activation=extend_schema(
        tags=["Владелец компании"],
        description="Активация пользователя по uid и token",
        summary="Активация пользователя",
    ),
    me=[
        extend_schema(
            tags=["Владелец компании"],
            description="Получение информации о текущем пользователе",
            summary="Получение информации о текущем пользователе",
            methods=["GET"],
        ),
        extend_schema(
            tags=["Владелец компании"],
            description="Изменение информации о текущем пользователе",
            summary="Изменение информации о текущем пользователе",
            methods=["PUT"],
        ),
        extend_schema(
            tags=["Владелец компании"],
            description="Частичное обновление информации о текущем пользователе",
            summary="Частичное обновление информации о текущем пользователе",
            methods=["PATCH"],
        ),
        extend_schema(
            tags=["Владелец компании"],
            description="Удаление текущего пользователя",
            summary="Удаление текущего пользователя",
            methods=["DELETE"],
        ),
    ],
    resend_activation=extend_schema(
        tags=["Владелец компании"],
        description="Запрос на повторное отправление кода активации",
        summary="Повторная отправка кода активации",
    ),
    reset_password=extend_schema(
        tags=["Владелец компании"],
        description="Запрос на сброс пароля пользователя",
        summary="Сброс пароля пользователя",
    ),
    reset_password_confirm=extend_schema(
        tags=["Владелец компании"],
        description="Подтверждение сброса пароля пользователя",
        summary=" Подтверждение сброса пароля",
    ),
    reset_username=extend_schema(
        tags=["Владелец компании"],
        description="Запрос на смену имени пользователя",
        summary="Смена имени пользователя",
    ),
    reset_username_confirm=extend_schema(
        tags=["Владелец компании"],
        description="Подтверждение смены имени пользователя",
        summary="Подтверждение смены имени пользователя",
    ),
    set_password=extend_schema(
        tags=["Владелец компании"],
        description="Установка нового пароля пользователя",
        summary="Установка нового пароля",
    ),
    set_username=extend_schema(
        tags=["Владелец компании"],
        description="Установка нового имени пользователя.",
        summary="Установка нового имени пользователя",
    ),
)
class CompanyOwnerViewset(CustomUserViewSet):
    """
    Вьюсет предоставляет функционал для регистрации пользователя
    в качестве владельца компании автосервиса. Вьюсет создает
    пользоаателя, добавляет его в группу владельцев автосервиса,
    создает Компанию и устанавливает ее владельца
    """

    company_serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        response: Response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = self.get_user_from_response(response)
            self.user_add_group(user)
            self.create_company(request, user=user, *args, **kwargs)
        return response

    def get_user_from_response(self, response: Response) -> CustomUser:
        user_id = response.data.get("id")
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist as e:
            print(f"user with id {user_id} does not exist", e)
            raise CustomUser.DoesNotExist from e
        return user

    def user_add_group(self, user: CustomUser):
        group, _ = Group.objects.get_or_create(name='company_owners')
        user.groups.add(group)
        user.save()

    def create_company(self, request, *args, user: CustomUser, **kwargs) -> Response:
        data = {}
        data['title'] = request.data.get("company_name")
        data['description'] = request.data.get("description")
        data['legal_address'] = request.data.get("legal_address")
        data["owner"] = user.id
        serializer = self.company_serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
