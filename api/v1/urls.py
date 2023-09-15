from django.urls import path, include
from .autoservice import urls as urls_autoservice
from .core import urls as urls_core
from .cars import urls as urls_cars

urlpatterns = [
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core)),
    path('car/', include(urls_cars))
]
