from django.urls import path, include
from .autoservice import urls as urls_autoservice
from .core import urls as urls_core


urlpatterns = [
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core))
]
