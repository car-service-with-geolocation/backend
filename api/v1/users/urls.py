from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.routers import SimpleRouter

from .views import CustomUserActivation, CustomUserViewSet

router = SimpleRouter()

router.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    path(
        "users/activate/<slug:uid>/<slug:token>/",
        CustomUserActivation.as_view(),
        name="user_activation",
    ),
    path(
        "token/login/",
        extend_schema_view(
            post=extend_schema(
                tags=["Пользователь"],
                description="Выполняет запрос для авторизации пользователя",
                summary="Авторизация пользователя",
            )
        )(TokenCreateView.as_view()),
        name="login",
    ),
    path(
        "token/logout/",
        extend_schema_view(
            post=extend_schema(
                tags=["Пользователь"],
                description="Выполняет деавторизация для авторизованого пользователя",
                summary="Деавторизация пользователя",
            )
        )(TokenDestroyView.as_view()),
        name="logout",
    ),
    path("", include(router.urls)),
]
