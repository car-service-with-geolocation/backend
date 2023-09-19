from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters, generics, viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS 
 
from .filters import JobsFilter
from .serializers import JobsSerializer
from jobs.models import Jobs


class JobsList(generics.ListAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend) 
    filterset_class = JobsFilter 
    search_fields = ('name', )

class JobsDetail(generics.RetrieveAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
