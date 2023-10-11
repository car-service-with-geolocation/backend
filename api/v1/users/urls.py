from .views import CustomUserViewSet, CustomUserActivation
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(
    r'users',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    path('users/activate/<slug:uid>/<slug:token>/',
         CustomUserActivation.as_view(),
         name='user_activation'
         ),
    path('', include(router.urls)),
]
