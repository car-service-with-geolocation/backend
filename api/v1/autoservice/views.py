from rest_framework import viewsets
from autoservice.models import Company
from .serializers import CompanySerializer


class CompanyViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
