from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import TransportDetail, TransportList

router = SimpleRouter()
router.register(
    r'company',
    views.CompanyViewset,
    basename='company'
)
router.register(
    r'service',
    views.AutoServiceViewSet,
    basename='service'
)
router.register(
    r'service/(?P<autoservice_id>\d+)/feedback',
    views.FeedbackViewSet,
    basename='feedback'
)

urlpatterns = [
    path('', include(router.urls)),
    path('car_models', TransportList.as_view(), name='transport-list'),
    path('car_models/<int:pk>/',
         TransportDetail.as_view(),
         name='transport-detail'
         ),
]
