from .views import CustomUserViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(
    r'users',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
]
