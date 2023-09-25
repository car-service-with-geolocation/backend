from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings

router = SimpleRouter()
router.register(
    r'company',
    views.CompanyViewset,
    basename='company'
)
#router.register(
#    r'service/(?P<autoservice_id>\d+)/feedback',
#    views.FeedbackViewSet,
#    basename='feedback'
#)

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
