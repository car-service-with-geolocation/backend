from django.urls import path

from .views import OrderDetailAPIView, OrderListAPIView

urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
