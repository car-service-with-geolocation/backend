from django.contrib import admin
from django.conf import settings

from order.models import Order


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



admin.site.register(Order, OrderAdmin)
