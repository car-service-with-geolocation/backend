from rest_framework import status, views
from rest_framework.response import Response

from core.utils import get_geoip_from_request

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema(
    tags = ["Геолокация"],
    methods = ["GET"],
)
@extend_schema_view(
    get=extend_schema(description="Получить текущую геолокацию клиента по IP из запроса", summary = "Получить IP")
)
class MyGeoIPApiView(views.APIView):
    def get(self, request):
        geoip = get_geoip_from_request(request)
        if geoip is None:
            return Response(
                {"geoip_error": "Произошла ошибка при получении геолокации."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            geoip,
            status=status.HTTP_200_OK
        )
