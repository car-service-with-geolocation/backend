from django.db.models import F, Avg, Count
from django.db.models.functions import (
    ASin,
    Cos,
    Power,
    Radians,
    Sin,
    Sqrt
)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.permissions import AllowAny

from autoservice.models import AutoService, Company, Job, Transport, Image
from core.utils import is_float

from .filters import TransportsFilter, JobsFilter
from .serializers import (
    AutoServiceSerializer,
    CompanySerializer,
    FeedbackSerializer,
    ListAutoServiceSerializer,
    TransportsSerializer,
    JobsSerializer
)
from .permissions import IsAuthorOrAdminReadOnly

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    tags = ["Автосервисы"],
    methods = ["GET"],
)
@extend_schema_view(
    get = extend_schema(description = "Получить список всех моделей автомобилей",
                        summary = "Получить список моделей а/м ")
)
class TransportList(generics.ListAPIView):

    # Вьюсет для чтения информации о компаниях по ремонту авто.

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TransportsFilter
    search_fields = ('brand',)


@extend_schema(
    tags = ["Автосервисы"],
    methods = ["GET"],
)
@extend_schema_view(
    get = extend_schema(description = "Получить информацию о модели автомобиля по id",
                        summary = "Получить информацию а/м по id"))

class TransportDetail(generics.RetrieveAPIView):

    # Вьюсет для чтения информации о компаниях по ремонту авто.

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer


@extend_schema(
    tags = ["Автосервисы"],
    methods = ["GET"],
)
@extend_schema_view(
        list=extend_schema(
            description = "Получить список компаний по ремонту авто",
            summary = "Получить список компаний",
            tags=["Автосервисы"]
        ),
        retrieve=extend_schema(
            description = "Получить информацию о компании по ремонту авто",
            summary = "Получить информация о компании по id",
            tags=["Автосервисы"]
        )
    )
class CompanyViewset(viewsets.ReadOnlyModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

@extend_schema(
    tags = ["Автосервисы"],
    methods = ["GET"],
)
@extend_schema_view(
        list = extend_schema(
            summary = "Получить список автосервисов.",
            description = "Получить список автосервисов , param: latitude",
            tags = ["Автосервисы"]
        ),
        retrieve = extend_schema(
            summary = "Получить детали автосервиса по id",
            description = "Получить детали автосервиса по id",
            tags = ["Автосервисы"]
        )
    )
class AutoServiceViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):

    #ViewSet для получения списка автосервисов
    #param: latitude

    serializer_class = AutoServiceSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in 'list':
            return ListAutoServiceSerializer
        return AutoServiceSerializer

    def get_queryset(self):
        queryset = (
            AutoService
            .objects
            .select_related("geolocation")
            .annotate(
                rating=Avg('feedback__score'),
                votes=Count('feedback__score')
            )
            .order_by('-rating')
        )
        if (
                'latitude' in self.request.query_params
                and 'longitude' in self.request.query_params
                and is_float(self.request.query_params['latitude'])
                and is_float(self.request.query_params['longitude'])
        ):
            lat = float(self.request.query_params['latitude'])
            lon = float(self.request.query_params['longitude'])
            queryset = queryset.annotate(
                distance=(
                        2 * 6371
                        * ASin(Sqrt(
                    Power(Sin((
                                      Radians(F('geolocation__latitude')) - Radians(lat)
                              ) / 2), 2)
                    + Cos(Radians(lat))
                    * Cos(Radians(F('geolocation__latitude')))
                    * Power(Sin((
                                        Radians(F('geolocation__longitude')) - Radians(lon)
                                ) / 2), 2)
                ))
                )
            ).order_by('distance', '-rating')
        return queryset

@extend_schema(
    tags = ["Отзывы"],
    methods = ["GET", "POST", "PATCH", "DELETE"],
)
@extend_schema_view(
    list = extend_schema(
        summary = "Получить отзывы об автосервисе",
        description = "Получить список отзывыв об автосервисе необходимо указать id автосервиса",
        tags = ["Отзывы"]
    ),
    create = extend_schema(
        summary = "Создать отзыв об автосервисе",
        description = "Создать отзыв об автосервисе необходимо указать id автосервиса",
        tags = ["Отзывы"]
    ),
    retrieve = extend_schema(
        summary = "Получить детали отзыва об автосервисе",
        description = "Получить детали отзыва об автосервисе необходимо указать id автосервиса и id отзыва",
        tags = ["Отзывы"]
    ),
    update = extend_schema(
        summary = "Изменить отзыв об автосервисе ",
        description = "Изменить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags = ["Отзывы"]
    ),
    partial_update = extend_schema(
        summary = "Изменить отзыв об автосервисе.",
        description = "Изменить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags = ["Отзывы"]
    ),
    destroy = extend_schema(
        summary = "Удалить отзыв об автосервисе",
        description = "Удалить отзыв об автосервисе необходимо указать id автосервиса и id отзыва",
        tags = ["Отзывы"]
    )
)
class FeedbackViewSet(viewsets.ModelViewSet):

    # ViewSet для модели отзывов Feedback.

    serializer_class = FeedbackSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthorOrAdminReadOnly]

    def get_autoservice(self):
        return get_object_or_404(
            AutoService,
            pk=self.kwargs.get('autoservice_id')
        )

    def get_queryset(self):
        return self.get_autoservice().feedback.all()

    def perform_create(self, serializer):
        feedback = serializer.save(
            author=self.request.user,
            autoservice=self.get_autoservice()
        )

        for file in self.request.FILES.getlist('images'):
            image = Image.objects.create(image=file)
            feedback.images.add(image)


class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = JobsFilter
    search_fields = ('name', )


@extend_schema(
    tags = ["Работы"],
    methods = ["GET"],
)
@extend_schema_view(
    get=extend_schema(description = "Получить список всех работ", summary = "Получить все данные")
)
class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = JobsFilter
    search_fields = ('name', )

@extend_schema(
    tags=["Работы"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(description = "Получить подробную информацию о конкретной работе", summary = "Получить данные по id")
)
class JobsDetail(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
