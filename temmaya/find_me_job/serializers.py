from rest_framework import serializers
from .models import Sector, UserCVSector, Logo, Job

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
    
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'low_salary', 'high_salary']

class FullSectorSerializer(serializers.ModelSerializer):
    main_logo = LogoSerializer(many=True, read_only=True)
    logos = LogoSerializer(many=True, read_only=True)
    jobs = JobSerializer(many=True, read_only=True)
    user_cv = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = ['id', 'name', 'low_salary', 'high_salary', 'description', 
                  'main_logo', 'logos', 'jobs', 'user_cv']
    
    def get_user_cv(self, obj):
        # Get the current user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user_cv = UserCVSector.objects.filter(user=request.user, sector=obj).first()
            if user_cv:
                return UserCVSectorSerializer(user_cv).data
        return None
    