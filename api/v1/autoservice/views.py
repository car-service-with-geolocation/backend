from core.utils import is_float
from django.db.models import Avg, F, Value
from django.db.models.functions import Abs, Sqrt, Radians, Cos, Sin, ASin, Power
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, status
from rest_framework.response import Response

from autoservice.models import (
    AutoService,
    Company,
    Feedback
)
from .serializers import (
    AutoServiceSerializer,
    CompanySerializer,
    FeedbackSerializer,
)


class CompanyViewset(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для чтения информации о компаниях по ремонту авто.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class RetriveAutoServiceApiView(views.APIView):

    def get(self, request, id):
        queryset = get_object_or_404(AutoService, id=id)
        return Response(
            AutoServiceSerializer(
                queryset,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK
        )


class AutoServiceFromGeoIPApiView(views.APIView):
    """
    ApiView для получения автосервисов.
    Автосервисы отсортированы по расстоянию до клиента.
    """
    def get(self, request):
        queryset = AutoService.objects.select_related("geolocation").order_by('-rating')
        #if 'city' in request.query_params:
        #    queryset = AutoService.objects.filter(
        #        city=request.query_params['city']
        #    )
        if (
            'latitude' in request.query_params
            and 'longitude' in request.query_params
            and is_float(request.query_params['latitude'])
            and is_float(request.query_params['longitude'])
        ):
            
            lat = float(request.query_params['latitude'])
            lon = float(request.query_params['longitude'])
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
        return Response(
            AutoServiceSerializer(
                queryset,
                context={"request": request},
                many=True
            ).data,
            status=status.HTTP_200_OK
        )


class FeedbackViewSet(viewsets.ModelViewSet):
    '''ViewSet для модели Feedback'''
    serializer_class = FeedbackSerializer

    def get_autoservice(self):
        return get_object_or_404(
            AutoService,
            pk=self.kwargs.get('autoservice_id')
        )

    def get_queryset(self):
        return self.get_autoservice().feedbacks.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            autoservice=self.get_autoservice()
        )
