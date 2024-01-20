from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from order.models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    tags=["Заказы"],
    methods=["POST", "GET"],
    description="API для управления списком заказов."
)
@extend_schema_view(
    get=extend_schema(description="Получить список всех заказов", summary="Получить данные"),
    post=extend_schema(description="Создать новый заказ", summary="Отправить данные")
)
class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


@extend_schema(
    tags=["Заказы"],
    methods=["POST", "GET"],
    description="API для управления списком заказов.",
)
@extend_schema_view(
    get=extend_schema(
        description="Получить список заказов текущего пользователя",
        summary="Получить данные текущего пользователя",
    ),
)
class CurrentUserOrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(owner=self.request.user)
        return queryset


@extend_schema(
    tags=["Заказы"],
    methods=["GET", "PUT", "PATCH", "DELETE"],
    description="API для управления отдельным заказом."
)
@extend_schema_view(
    get=extend_schema(description="Получить информацию о конкретном заказе по его ID", summary="Получить данные по id"),
    put=extend_schema(description="Обновить информацию о конкретном заказе по его ID", summary="Обновить данные по id"),
    patch=extend_schema(description="Изменить часть информации о заказе по его ID", summary="Изменить данные по id"),
    delete=extend_schema(description="Удалить заказ по его ID", summary="Удалить данные по id")
)
class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
