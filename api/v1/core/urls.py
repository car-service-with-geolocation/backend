from django.urls import path

from . import views

urlpatterns = [
    path('geoip/my/', views.MyGeoIPApiView.as_view(), name='geoip_my')
]
