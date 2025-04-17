from .models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from uuid import uuid4

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'first_name', 'user_type', 'prof_pic']

class PassCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        with transaction.atomic():
            # user = super().create(validated_data)
            user = self.Meta.model(**validated_data)

            user.email = email.lower()
            
            if password is not None:
                user.set_password(password)

            user.save()
            return user


# class GoogleSocialAuthSerializer(serializers.Serializer):
#     auth_token = serializers.CharField()
#     print(auth_token)
#     def validate_auth_token(self, auth_token):
#         user_data = google.Google.validate(auth_token)
#         try:
#             user_data['sub']
#         except:
#             raise serializers.ValidationError(
#                 'The token is invalid or expired. Please login again.'
#             )

#         if user_data['aud'] != '638120310022-e66gabge1dggjjf6skldfh4opbivng9f.apps.googleusercontent.com':

#             raise AuthenticationFailed('oops, who are you?')

#         user_id = user_data['sub']
#         email = user_data['email']
#         name = user_data['name']
#         provider = 'google'
#         print(f"seri {email}")
#         return register_social_user(
#             provider=provider, user_id=user_id, email=email, name=name)

class ChangePasswordSerializer(serializers.Serializer):

    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=2, max_length=68, write_only=True)

class GoogleLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    name = serializers.CharField(max_length=100)

