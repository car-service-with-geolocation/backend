from django.urls import path, include
from .autoservice import urls as urls_autoservice


urlpatterns = [
    path('autoservice/', include(urls_autoservice))
]
