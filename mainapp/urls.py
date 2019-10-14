from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *
from mainapp import signals

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='mainapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mainapp/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user/<str:username>/', ProfileView.as_view(), name='profile'),
    path('user/<str:username>/', MyProfileView.as_view(), name='my-profile'),
    path('edit-profile', ProfileEditView.as_view(), name='profile-edit'),
]
