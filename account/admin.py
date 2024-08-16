from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, OtpCode
from .forms import UserChangeForm

admin.site.register(OtpCode)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    
    list_display = ('phone_number', 'first_name', 'last_name', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'first_name', 'last_name', 'email', 'ssn', 'wallet_amount')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number' , 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)