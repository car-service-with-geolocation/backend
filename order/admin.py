from django.contrib import admin

from order.models import Order

class OrderAdmin(admin.ModelAdmin):
    """
    Модель Заявка(Order) в админ панеле.
    """
    list_display = (
        'owner', 'car', 'info', 'task', 'jobs', 'image'
    )

admin.site.register(Order, OrderAdmin)
