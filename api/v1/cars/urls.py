from django.urls import include, path 
from rest_framework.routers import DefaultRouter 
 
 
from cars.views import TransportList, TransportDetail, CarsList, CarsDetail

urlpatterns = [
    path('transports/', TransportList.as_view(), name='transport-list'),
    path('transports/<int:pk>/', TransportDetail.as_view(), name='transport-detail'),
    path('cars/', CarsList.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarsDetail.as_view(), name='car-detail'),
]