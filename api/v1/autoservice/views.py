from rest_framework import viewsets, views
from autoservice.models import Company
from .serializers import CompanySerializer


class CompanyViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class AutoServiceFromGeoIPApiView(views.APIView):

    def get(self, request, latitude, longitude):
        pass
