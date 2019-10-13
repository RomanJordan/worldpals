from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=50, null=True, blank=True)
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    biography = models.TextField(default='Add something about yourself here!')
    
    
    def __str__(self):
        return str(self.user)

    