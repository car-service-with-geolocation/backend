from django.contrib import admin

from cars.models import Cars, Transport

@admin.register(Cars) 
class CarsAdmin(admin.ModelAdmin): 
    list_display = ('id', 'owner', 'car', 'color', 'vin', 'number_of_car', 
                    'odometr', 'year', 'last_service_date') 
    list_filter = ('owner',) 
    search_fields = ('owner',)

@admin.register(Transport) 
class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model') 
    list_filter = ('brand',) 
    search_fields = ('brand',)