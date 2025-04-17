from django.shortcuts import render
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import (UserSerializer, PassCodeSerializer,
                          RegisterUserSerializer, GoogleLoginSerializer,
                          ChangePasswordSerializer, SetNewPasswordSerializer, 
                          ResetPasswordEmailRequestSerializer,
                          )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import User
from rest_framework import generics, status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from decouple import config
from .utils import username_generator, email_sender
from .utils import email_by_template
# Create your views here.

class RegisterUserView(APIView):
     permission_classes=[AllowAny]

     def post(self, request):
            reg_serializer=RegisterUserSerializer(data=request.data)
            if reg_serializer.is_valid():

                new_user=reg_serializer.save()
                if new_user:
                    refresh = RefreshToken.for_user(new_user)

                    return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                                    },status=201)
            return Response(reg_serializer.errors, status=400)


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"detail": "old password is wrong!"}, status=400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'detail': 'Password updated successfully!',
            }

            return Response(response, status=200)

        return Response(serializer.errors, status=400)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                # ?token=cgshfm-8090070509dd553ceef551623db47e7e&uidb64=MTA/
                # absurl = config("ALLOWED_HOST")+f"/api/users/password-reset-confirm?token={token}&uidb64={uidb64}"
                absurl = config("FRONTEND_URL")+f"password-recover?token={token}&uidb64={uidb64}"
                email_by_template(subject="",
                            ctx={'username':user.username, 'absurl':absurl
                                 },

                            template_path='forgot-password.html', to=[email])
                # email_body = f'''
                # Hello {user.username}, \n Use link below to reset your passworddddddddddddd  n\'
                # {absurl}'''
           
                # email_sender(email=email, title='Reset your passsword', body=email_body)
                return Response({'detail': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            return Response({"detail":"email is wrong!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(GenericAPIView):

    def post(self, request):
        serializer=SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password=serializer.validated_data['password']

            token = request.GET.get("token")
            uidb64=request.GET.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'detail': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            return Response({'detail': 'Password reset successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user

        serializer=UserSerializer(user)

        return Response({"data":serializer.data}, status=200)
    

class GoogleLoginView(APIView):
    def post(self, request):
        serializer=GoogleLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                print(f"error from login {e}")
                name = serializer.validated_data['name']
                username = username_generator(name=name)
                user = User.objects.create(username=username, email=email)
                user.set_password(config('PASSWORD_USER'))
                user.save()
                
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=200)
        
        return Response({"detail":serializer.errors}, status=400)
