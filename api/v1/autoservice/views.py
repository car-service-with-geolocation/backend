from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, status
from rest_framework.response import Response

from autoservice.models import Company, AutoService
from feedback.models import Feedback
from .serializers import (
    AutoServiceSerializer,
    AutoServiceGeoIPSerializer,
    CompanySerializer,
    FeedbackSerializer,
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
            ).annotate(rating=Avg('feedback_score'))
        if (
            'latitude' in request.query_params
            and 'longitude' in request.query_params
            and request.query_params['latitude'].isnumeric()
            and request.query_params['longitude'].isnumeric()
        ):
            print(1)
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


class FeedbackViewSet(viewsets.ModelViewSet):
    '''ViewSet для модели Feedback'''
    serializer_class = FeedbackSerializer

    def get_autoservice(self):
        return get_object_or_404(
            AutoService,
            pk=self.kwargs.get('autoservice_id')
        )

    def get_queryset(self):
        return self.get_autoservice().feedbacks.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            autoservice=self.get_autoservice()
        )
