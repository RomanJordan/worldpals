from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


admin.site.register(CustomUser)
admin.site.register(Profile)
#admin.site.register(UserAdmin)