from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from order.models import Order, OrderImages

from .serializers import OrderImagesSerializer, OrderSerializer


@extend_schema(
    tags=["Заказы"],
    methods=["POST", "GET"],
    description="API для управления списком заказов.",
)
@extend_schema_view(
    get=extend_schema(
        description="Получить список всех заказов", summary="Получить данные"
    ),
    post=extend_schema(description="Создать новый заказ", summary="Отправить данные"),
)
class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()


@extend_schema(
    tags=["Заказы"],
    methods=["GET"],
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
    parser_class = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Order.objects.filter(owner=self.request.user)
        return queryset

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["owner"] = request.user.id
        file_fields = list(request.FILES.keys())

        serializer = self.get_serializer(data=data, file_fields=file_fields)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@extend_schema(
    tags=["Заказы"],
    methods=["GET", "PUT", "PATCH", "DELETE"],
    description="API для управления отдельным заказом.",
)
@extend_schema_view(
    get=extend_schema(
        description="Получить информацию о конкретном заказе по его ID",
        summary="Получить данные по id",
    ),
    put=extend_schema(
        description="Обновить информацию о конкретном заказе по его ID",
        summary="Обновить данные по id",
    ),
    patch=extend_schema(
        description="Изменить часть информации о заказе по его ID",
        summary="Изменить данные по id",
    ),
    delete=extend_schema(
        description="Удалить заказ по его ID", summary="Удалить данные по id"
    ),
)
class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
