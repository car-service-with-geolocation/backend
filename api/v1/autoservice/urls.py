from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views
from .views import (
    CompanyOwnerView,
    JobsDetail,
    JobsList,
    TransportDetail,
    TransportList,
)

router = SimpleRouter()
default_router = DefaultRouter()
router.register(r"company", views.CompanyViewset, basename="company")
router.register(r"service", views.AutoServiceViewSet, basename="service")
router.register(
    r"service/(?P<autoservice_id>\d+)/feedback",
    views.FeedbackViewSet,
    basename="feedback",
)

urlpatterns = [
    path("car_models", TransportList.as_view(), name="transport-list"),
    path("car_models/<int:pk>/", TransportDetail.as_view(), name="transport-detail"),
    path("", JobsList.as_view(), name="jobs-list"),
    path("<int:pk>/", JobsDetail.as_view(), name="jobs-detail"),
    path("me/", CompanyOwnerView.as_view(), name="company-owner"),
    path("", include(router.urls)),
    path("", include(default_router.urls)),
]
