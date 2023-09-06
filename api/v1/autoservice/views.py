from rest_framework import viewsets, views, status
from rest_framework.response import Response
from autoservice.models import Company, AutoService
from .serializers import CompanySerializer, AutoServiceSerializer


class CompanyViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class AutoServiceFromGeoIPApiView(views.APIView):

    def get(self, request):

        def val_geo_size(data_obj):
            return data_obj['geo_size']

        if (
            'latitude' in request.query_params
            and 'longitude' in request.query_params
        ):
            data = AutoServiceSerializer(
                AutoService.objects.all(),
                context={"request": request},
                many=True
            ).data
            data = sorted(data, key=val_geo_size, reverse=False)
            return Response(
                data, status=status.HTTP_200_OK
            )
        return Response(
            {
                "geoip_error": (
                    "Невозможно получить список автосервисов. "
                    "Ошибка при задании геолокации."
                )
            },
            status=status.HTTP_204_NO_CONTENT
        )
