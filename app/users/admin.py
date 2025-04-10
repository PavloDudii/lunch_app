"""
Custom Django Admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    """Admin page for users"""
    ordering = ['id']
    list_display = ['email', 'name', 'id']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Permissions',
            {'fields': ('is_active',
                        'is_staff',
                        'is_restaurant_staff',
                        'is_superuser',
                        )}
        )
    )
    add_fieldsets = (
        (None, {
            'fields': ('email',
                       'name',
                       'password1',
                       'password2',
                       'is_active',
                       'is_staff',
                       'is_restaurant_staff',
                       'is_superuser'),
        }),
    )


admin.site.register(User, UserAdmin)
