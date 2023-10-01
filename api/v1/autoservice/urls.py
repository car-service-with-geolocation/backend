from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
