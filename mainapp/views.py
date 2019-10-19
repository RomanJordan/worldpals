from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import ListView, DetailView, UpdateView
from .models import User, Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.contrib.messages import constants as messages
from django.contrib import messages, auth

def index(request):
    return render(request, 'mainapp/index.html')

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email__iexact=request.POST['email']).exists() or User.objects.filter(username__iexact=request.POST['username']).exists():
            messages.warning(request, 'This email or username is already taken')
            return redirect('register')

        user_form = CustomUserCreationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request, 'Account created')
            return redirect('login')
        else:
            print(user_form.errors)
            return render(request, 'mainapp/register.html', {'form': user_form})

class ProfileView(DetailView):
    model = Profile
    template_name = 'mainapp/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return Profile.objects.filter(user__username=self.kwargs['username']) 

class MyProfileView(DetailView):
    model = User
    template_name = 'mainapp/profile.html'

@login_required
def profile(request):
    return render(request, 'mainapp/my-profile.html')

class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'mainapp/profile-edit.html'
    context_object_name = 'profile'
    fields = ('image','biography',)
    
    def get_object(self, queryset=None):
        return self.request.user.profile

    def edit_profile(request):
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # request.FILES is show the selected image or file

