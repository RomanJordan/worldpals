from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_OPTIONS = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender'),
        ('prefer_not_to_say', 'Prefer not to say')
    ]

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=100, unique=True, 
    help_text='Required. Username must be less than 50 characters')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20,choices=GENDER_OPTIONS, blank=False, default='')
    country = CountryField(default='US')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
        
    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.username
            self.slug = slugify(value, allow_unicode=True)
        super().save()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    biography = models.TextField(default='Add something about yourself here!')
    
    
    def __str__(self):
        return str(self.user)

    