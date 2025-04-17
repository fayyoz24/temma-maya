"""
URL configuration for temmaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .custom_views import CustomTokenObtainPairView
from .settings import DEBUG
from decouple import config


admin_url = 'admin'
if not DEBUG:
    admin_url = config('ADMIN_URL')


urlpatterns = [
    # swagger
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path(admin_url, admin.site.urls),
    path('api/find-me-job/', include('find_me_job.urls')),
    path('api/users/', include('users.urls')),
    path('api/blog/', include('blog.urls')),
]
