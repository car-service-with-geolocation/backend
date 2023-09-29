from django.contrib import admin

from cars.models import Cars, Transport


class CarsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'owner',
                    'car',
                    'color',
                    'vin',
                    'number_of_car',
                    'odometr',
                    'year',
                    'last_service_date'
                    )
    list_filter = ('owner', )
    search_fields = ('owner', )


class TransportAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'brand',
                    'model'
                    )
    list_filter = ('brand', )
    search_fields = ('brand', )


admin.site.register(Cars)
admin.site.register(Transport)
