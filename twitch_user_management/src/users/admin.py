from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                )
            },
        ),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'role',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'role', 'first_name', 'last_name', 'password1', 'password2'),
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return False
