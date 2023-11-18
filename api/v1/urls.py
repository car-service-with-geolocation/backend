from django.urls import include, path

from .autoservice import urls as urls_autoservice
from .core import urls as urls_core
from .users import urls as urls_users
from .order import urls as urls_order

urlpatterns = [
    path('autoservice/', include(urls_autoservice)),
    path('core/', include(urls_core)),
    path('orders/', include(urls_order)),
    path('auth/', include(urls_users))
]
