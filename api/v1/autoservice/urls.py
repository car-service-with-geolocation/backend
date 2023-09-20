from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(
    r'company',
    views.CompanyViewset,
    basename='company'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'service/',
        views.AutoServiceFromGeoIPApiView.as_view(),
        name='service'
    ),
    path(
        'service/<int:id>/',
        views.RetriveAutoServiceApiView.as_view(),
        name='service-id'
    )
]
