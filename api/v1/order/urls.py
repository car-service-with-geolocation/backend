from django.urls import path

from .views import OrderDetailAPIView, OrderListAPIView, CurrentUserOrderListAPIView

urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list'),
    path('me/', CurrentUserOrderListAPIView.as_view(), name='current-user-order-list'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
