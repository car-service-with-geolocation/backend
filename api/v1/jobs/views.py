from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters, generics, viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS 
 
from .filters import JobsFilter
from .serializers import JobsSerializer
from autoservice.models import Job


class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend) 
    filterset_class = JobsFilter 
    search_fields = ('name', )

class JobsDetail(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
