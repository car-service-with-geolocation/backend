from django.urls import include, path

from .autoservice import urls as urls_autoservice
from .cars import urls as urls_cars
from .core import urls as urls_core
from .users import urls as urls_users
from .jobs import urls as urls_jobs

urlpatterns = [
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core)),
    path('car_models/', include(urls_cars)),
    path('jobs/', include(urls_jobs)),
    path('auth/', include(urls_users)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
