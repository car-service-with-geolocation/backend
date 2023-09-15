from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters, generics, viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS 
 
from cars.filters import TransportsFilter
from cars.permissions import IsOwnerOrReadOnly 
from cars.serializers import CarsSerializer, TransportsSerializer
from cars.models import Cars, Transport


class TransportList(generics.ListAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend) 
    filterset_class = TransportsFilter 
    search_fields = ('brand', 'model')

class TransportDetail(generics.RetrieveAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer

class CarsList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly) 
    serializer_class = CarsSerializer

    def get_queryset(self):
        return Cars.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CarsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly) 
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer

    def get_object(self):
        return super().get_object()
