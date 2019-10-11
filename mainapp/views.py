from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import ListView, DetailView
from .models import CustomUser, Profile

def index(request):
    return render(request, 'mainapp/index.html')

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'mainapp/register.html'

class ProfileView(DetailView):
    model = CustomUser
    query_pk_and_slug = False
    template_name = 'mainapp/profile.html'

# class ProfileView(DetailView):
#     template_name = 'mainapp/profile.html'

#     def get_context_data(self, **kwargs):
#         context = super(ProfileView, self).get_context_data(**kwargs)
#         context