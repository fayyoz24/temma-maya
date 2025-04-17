from rest_framework import serializers
from .models import Sector, UserCVSector, Logo

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'name', 'image']

class SectorSerializer(serializers.ModelSerializer):
    main_logo = LogoSerializer(many=True, read_only=True)
    logos = LogoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description', 'low_salary', 'high_salary', 
                 'main_logo', 'logos', 'created_at', 'updated_at']

class UserCVSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCVSector
        fields = ['id', 'user', 'sector', 'cv', 'created_at', 'updated_at']
        read_only_fields = ['user', 'sector']
    
    def create(self, validated_data):
        # Both user and sector will be set in the view
        return super().create(validated_data)
    