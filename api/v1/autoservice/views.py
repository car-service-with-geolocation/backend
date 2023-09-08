from rest_framework import viewsets, views, status
from rest_framework.response import Response
from autoservice.models import Company, AutoService
from .serializers import (
    AutoServiceSerializer,
    AutoServiceGeoIPSerializer,
    CompanySerializer,
)


class CompanyViewset(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для чтения информации о компаниях по ремонту авто.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class AutoServiceFromGeoIPApiView(views.APIView):
    """
    ApiView для получения автосервисов.
    Автосервисы отсортированы по расстоянию до клиента.
    """
    def get(self, request):
        queryset = AutoService.objects.all()
        if 'city' in request.query_params:
            queryset = AutoService.objects.filter(
                city=request.query_params['city']
            )
        if (
            'latitude' in request.query_params
            and 'longitude' in request.query_params
            and request.query_params['latitude'].isnumeric()
            and request.query_params['longitude'].isnumeric()
        ):
            return Response(
                sorted(
                    AutoServiceGeoIPSerializer(
                        queryset,
                        context={"request": request},
                        many=True
                    ).data,
                    key=lambda x: x['geo_size']
                ),
                status=status.HTTP_200_OK
            )
        return Response(
            AutoServiceSerializer(
                queryset,
                many=True
            ).data,
            status=status.HTTP_200_OK
        )
