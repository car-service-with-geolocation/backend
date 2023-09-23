from django.urls import path
# from rest_framework.routers import DefaultRouter
 
 
from .views import TransportList, TransportDetail, CarsList, CarsDetail

urlpatterns = [
    path('', TransportList.as_view(), name='transport-list'),
    path('<int:pk>/', TransportDetail.as_view(), name='transport-detail'),
    # Отключены на MVP @OrdinaryWorker
    # path('', CarsList.as_view(), name='car-list'),
    # path('<int:pk>/', CarsDetail.as_view(), name='car-detail'),
]