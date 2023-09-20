from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'company',
    views.CompanyViewset,
    basename='company'
)

# router.register(
#     r'(?P<autoservice_id>\d+)/feedbacks',
#     views.FeedbackViewSet,
#     basename='feedbacks'
# )

urlpatterns = [
    path('', include(router.urls)),
    path(
        'service/',
        views.AutoServiceFromGeoIPApiView.as_view(),
        name='service'
    ),
    path(
        'service/<int:id>/',
        views.RetriveautoServiceApiView.as_view(),
        name='service-id'
    )
]
