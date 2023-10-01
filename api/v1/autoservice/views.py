from django.db.models import F, Avg, Count, Min, Sum
from django.db.models.functions import ASin, Coalesce, Cos, Power, Radians, Sin, Sqrt
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from autoservice.models import AutoService, Company
from core.utils import is_float

from .serializers import (
    AutoServiceSerializer,
    CompanySerializer,
    FeedbackSerializer
)
from .permissions import IsAuthorOrAdminReadOnly


class CompanyViewset(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для чтения информации о компаниях по ремонту авто.
    """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class AutoServiceViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """
    ViewSet для получения списка автосервисов
    param: latitude
    """

    serializer_class = AutoServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = AutoService.objects.select_related(
                "geolocation"
            ).annotate(
                rating=Avg('feedback__score'),
                votes=Count('feedback__score')
        ).order_by('-rating')
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


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели отзывов Feedback
    """

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
        serializer.save(
            author=self.request.user,
            autoservice=self.get_autoservice()
        )
