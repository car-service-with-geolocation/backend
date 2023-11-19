from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from autoservice.models import Job

from .filters import JobsFilter
from .serializers import JobsSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view

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
