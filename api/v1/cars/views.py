from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from cars.models import Cars, Transport

from .filters import TransportsFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import CarsSerializer, TransportsSerializer


class TransportList(generics.ListAPIView):
    """
    Вьюсет для чтения информации о компаниях по ремонту авто.
    """

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TransportsFilter
    search_fields = ('brand', )


class TransportDetail(generics.RetrieveAPIView):
    """
    Вьюсет для чтения информации о компаниях по ремонту авто.
    """

    queryset = Transport.objects.all()
    serializer_class = TransportsSerializer


class CarsList(generics.ListCreateAPIView):
    """
    API-view функция для получения списка автомобилей владельца.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = CarsSerializer

    def get_queryset(self):
        return Cars.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarsDetail(generics.RetrieveAPIView):
    """
    API-view функция для получения данных об авто владельца.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer

    def get_object(self):
        return super().get_object()
