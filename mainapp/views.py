from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import ListView, DetailView
from .models import CustomUser, Profile
4

def index(request):
    return render(request, 'mainapp/index.html')

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'mainapp/register.html'

class ProfileView(DetailView):
    model = Profile
    template_name = 'mainapp/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return Profile.objects.filter(user__username=self.kwargs['username']) 

