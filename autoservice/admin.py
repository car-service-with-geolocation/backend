from django.contrib import admin
from .models import Company, AutoService


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class AutoServiceAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'latitude',
        'longitude',
    )
    search_fields = (
        'company',
    )
    empty_value_display = '-пусто-'


admin.site.register(Company, CompanyAdmin)
admin.site.register(AutoService, AutoServiceAdmin)
