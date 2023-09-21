from django.urls import path, include
from .autoservice import urls as urls_autoservice
from .core import urls as urls_core
from .cars import urls as urls_cars
from .users import urls as urls_users
from .jobs import urls as urls_jobs

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core)),
    path('car_models/', include(urls_cars)),
    path('users/', include(urls_users)),
    path('jobs/', include(urls_jobs)),
]
