from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class UserAccountAdmin(BaseUserAdmin):
    # Define admin model for custom User model with no email field
    fieldsets = ((None, {'fields': ('username', 'password')}),
                 (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}), (
                 ('Permissions'),
                 {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
                 (('Important dates'), {'fields': ('last_login', 'date_joined')}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2'), }),)
    # The forms to add and change user instances
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    list_display = ('username', 'work_id', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'employee_identification')
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    readonly_fields = ('last_login', 'date_joined')


# Register your models here.
admin.site.register(CustomUser, UserAccountAdmin)
