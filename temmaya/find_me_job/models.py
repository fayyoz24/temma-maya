from django.db import models
from .helper_functions import user_cv_dir
# Create your models here.

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    low_salary = models.IntegerField(default=0)    
    high_salary = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    main_logo = models.ManyToManyField('Logo', blank=True, related_name='sectors_main_logo')
    logos = models.ManyToManyField('Logo', blank=True, related_name='sectors_logos')
    jobs = models.ManyToManyField('Job', blank=True, related_name='jobs')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):  
        return self.name
    
class Logo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Logo {self.name}"
    
class Job(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    Low_salary = models.IntegerField(default=0)
    high_salary = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class UserCVSector(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_cv_sectors')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='user_cv_sectors')
    cv = models.FileField(upload_to=user_cv_dir)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.sector.name}"