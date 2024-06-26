"""
Django Admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    ordering = ['id']
    list_display = ('email', 'name', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'name',
                       'is_active',
                       'is_staff',
                       'is_superuser'),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Contact)
admin.site.register(models.Email)
admin.site.register(models.PhoneNumber)
admin.site.register(models.SocialMediaLink)
