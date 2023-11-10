from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import JobsDetail, JobsList, TransportDetail, TransportList

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
    path('car_models', TransportList.as_view(), name='transport-list'),
    path('car_models/<int:pk>/',
         TransportDetail.as_view(),
         name='transport-detail'
         ),
    path('jobs', JobsList.as_view(), name='jobs-list'),
    path('jobs/<int:pk>/', JobsDetail.as_view(), name='jobs-detail'),
    path('', include(router.urls)),
]
