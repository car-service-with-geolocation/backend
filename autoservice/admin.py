from django.contrib import admin
from .models import (
    AutoService,
    Company,
    City,
    GeolocationAutoService,
    GeolocationCity,
    Job,
    AutoserviceJob,
)


class CompanyAdmin(admin.ModelAdmin):
    """
    Кастомизация модели Company в админ панеле.
    """
    list_display = (
        'title',
        'legal_address',
    )
    search_fields = (
        'title',
    )
    empty_value_display = '-пусто-'


class CityAdmin(admin.ModelAdmin):
    """
    Кастомизация модели City в админ панеле.
    """
    list_display = (
        'rus_name', 'geolocation'
    )
    search_fields = (
        'rus_name',
    )


class GeolocationAutoServiceAdmin(admin.ModelAdmin):
    """
    Кастомизация модели GeolocationAutoService в админ панеле.
    """
    list_display = (
        'latitude', 'longitude'
    )


class GeolocationCityAdmin(admin.ModelAdmin):
    """
    Кастомизация модели геолокации города в админ панеле.
    """
    list_display = (
        'latitude', 'longitude'
    )


class AutoServiceAdmin(admin.ModelAdmin):
    """
    Кастомизация модели AutoService в админ панеле.
    """
    list_display = (
        'company',
        'geolocation',
    )
    search_fields = (
        'company',
    )
    empty_value_display = '-пусто-'


admin.site.register(
    GeolocationAutoService,
    GeolocationAutoServiceAdmin
)
admin.site.register(
    GeolocationCity,
    GeolocationCityAdmin,
)
admin.site.register(Company, CompanyAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(AutoService, AutoServiceAdmin)
admin.site.register(AutoserviceJob)
admin.site.register(Job)
