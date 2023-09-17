from django.urls import path, include
from .autoservice import urls as urls_autoservice
from .core import urls as urls_core
from .cars import urls as urls_cars
from .users import urls as urls_users


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core)),
    path('car/', include(urls_cars)),
    path('users/', include(urls_users)),
]
