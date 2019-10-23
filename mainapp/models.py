from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class User(AbstractUser):
    objects = CustomUserManager()
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
    help_text='Required.')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    birthdate = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20,choices=GENDER_OPTIONS, blank=False, default='')
    country = CountryField(default='US')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_friends(self):
        friends = Friend.objects.filter(User=self.User)
        return friends
        
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

class Friend(models.Model):
    original_user = models.ForeignKey(User, on_delete=models.CASCADE) #Who sent the friend request
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends') #Who received a friend request
    friends_since = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, default='requested')

