from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreateForm
from .models import CustomUser

admin.site.register(CustomUser)


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreateForm
    model = CustomUser
    list_display = UserAdmin.list_display + ('image',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image',)}),
    )


admin.register(CustomUser, CustomUserAdmin)
