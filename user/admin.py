from .models import User
from django import forms
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

def new_clean(self):
    email = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    
    if email and password:
        self.user_cache = authenticate(email=email, password=password)
        if self.user_cache is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                #params={'email': self.email_field.verbose_name},
            )
        else:
            self.confirm_login_allowed(self.user_cache)

    return self.cleaned_data

AuthenticationForm.clean = new_clean

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',  'is_staff', 'is_superuser', 'status',  'is_email_verified', 'joined_datetime')
    search_fields = ('email',)
    list_filter = ('status', 'is_email_verified', 'is_staff', 'is_superuser')
    ordering = ('email',)
