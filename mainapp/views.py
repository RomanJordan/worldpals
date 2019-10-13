from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import ListView, DetailView, UpdateView
from .models import User, Profile
from django.contrib.auth.decorators import login_required

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
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email is already taken')
            return redirect('mainapp/register.html')

        user_form = CustomUserCreationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            print(user_form.errors)
            return render(request, 'register', {'form': user_form})

class ProfileView(DetailView):
    model = Profile
    template_name = 'mainapp/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return Profile.objects.filter(user__username=self.kwargs['username']) 

class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'mainapp/profile-edit.html'
    context_object_name = 'profile'
    fields = '__all__'
    
    def get_object(self, queryset=None):
        return self.request.user.profile
