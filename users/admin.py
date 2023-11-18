from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (_('Личная информация'),
         {'fields': ('email', 'phone_number', 'first_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'email', 'phone_number', 'first_name')

    list_display_links = ('id', 'email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)


admin.site.register(CustomUser, CustomUserAdmin)
