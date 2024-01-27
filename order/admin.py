from django.contrib import admin
from django.conf import settings

from order.models import Order, OrderImages


class OrderAdmin(admin.ModelAdmin):
    """
    Модель Заявка(Order) в админ панеле.
    """
    list_display = (
        'pk',
        'owner',
        'car',
        'info',
        'task'
    )
    search_fields = (
        'owner',
        'car',
    )
    list_filter = ('owner',)
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


class OrderImagesAdmin(admin.ModelAdmin):
    """
    Модель Изображения к заявкам(OrderImages) в админ панеле.
    """
    list_display = (
        'pk',
        'upload_date',
        'order',
        'file',
    )
    search_fields = (
        'upload_date',
        'order',
    )
    list_filter = ('upload_date',)
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderImages, OrderImagesAdmin)
