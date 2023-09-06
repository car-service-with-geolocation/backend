from . import views
from django.urls import path


urlpatterns = [
    path('geoip/my/', views.MyGeoIPApiView.as_view(), name='geoip_my')
]
