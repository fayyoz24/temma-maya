from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# import question.models
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=100, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    USER_TYPE_CHOICES = [('L', 'LAWYER'), ('B', 'DUO_BOOKIE'),
                      ('A', 'ADMIN'), ('U', 'COMMON_USER'), ('P', 'PARTNER')]
    prof_pic = models.URLField(null=True, blank=True)
    # Default user_type must be defined to enforce security
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, verbose_name="User Type", default='U')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.username

# E-mail adres

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)  # Store IP addresses
    created_at = models.DateTimeField(auto_now_add=True)  # Track when it was added

    def __str__(self):
        return self.ip_address