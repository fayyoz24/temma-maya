from django.urls import path
from .views import (
    ChangePasswordView, RegisterUserView,
    GoogleLoginView,
    SetNewPasswordAPIView, RequestPasswordResetEmail,
     UserDetailView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from temmaya.custom_views import CustomTokenObtainPairView

urlpatterns = [
    path("signup", RegisterUserView.as_view(), name="signup"),
    # path("refer-friend", ReferUserView.as_view(), name="refer-friend"),
    path("google-login", GoogleLoginView.as_view(), name="google-login"),
    path("user-detail", UserDetailView.as_view(), name="user-detail"),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view()),
    path('password-reset/', RequestPasswordResetEmail.as_view(), name='password_reset'),
    path('password-reset-confirm', SetNewPasswordAPIView.as_view(), name='password_reset_confirm')
]