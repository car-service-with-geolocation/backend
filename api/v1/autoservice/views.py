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

        if (
            'latitude' in request.query_params
            and 'longitude' in request.query_params
            and request.query_params['latitude'].isnumeric()
            and request.query_params['longitude'].isnumeric()
        ):
            return Response(
                sorted(
                    AutoServiceGeoIPSerializer(
                        AutoService.objects.all(),
                        context={"request": request},
                        many=True
                    ).data,
                    key=lambda x: x['geo_size']
                ),
                status=status.HTTP_200_OK
            )
        return Response(
            AutoServiceSerializer(
                AutoService.objects.all(),
                many=True
            ).data,
            status=status.HTTP_200_OK
        )
