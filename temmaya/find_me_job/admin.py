from django.contrib import admin

# Register your models here.
from .models import Sector, Logo, Job, UserCVSector
admin.site.register(Sector)
admin.site.register(Logo)
admin.site.register(Job)