from .views import CustomUserViewSet, CustomUserActivation
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
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
    path('token/login/',
         TokenCreateView.as_view(),
         name='login'
         ),
    path('token/logout/',
         TokenDestroyView.as_view(),
         name='logout'
         ),
    path('', include(router.urls)),
]
