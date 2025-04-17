from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Sector, UserCVSector
from .serializers import SectorSerializer, UserCVSectorSerializer, FullSectorSerializer
# Create your views here.
class FullSectorListAPIView(APIView):
    """
    API view for listing all sectors
    """
    def get(self, request):
        sectors = Sector.objects.all()
        serializer = FullSectorSerializer(sectors, many=True, context={'request': request})
        return Response(serializer.data)
    
class SectorListAPIView(APIView):
    """
    API view for listing all sectors
    """
    def get(self, request):
        sectors = Sector.objects.all()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

class SectorDetailAPIView(APIView):
    """
    API view for retrieving a single sector
    """
    def get(self, request, sector_id):
        sector = get_object_or_404(Sector, pk=sector_id)
        serializer = SectorSerializer(sector)
        return Response(serializer.data)
    
class UserCVSectorListAPIView(APIView):
    """
    API view for listing and creating CV uploads
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get all CV uploads for the current user
        user_cvs = UserCVSector.objects.filter(user=request.user)
        serializer = UserCVSectorSerializer(user_cvs, many=True)
        return Response(serializer.data)

# class UserCVSectorCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, sector_id):
#         # Check if user already has a CV for this sector
#         existing_cv = UserCVSector.objects.filter(
#             user=request.user,
#             sector_id=sector_id
#         ).first()
        
#         if existing_cv:
#             # Update the existing CV
#             existing_cv.cv = request.data.get('cv')
#             existing_cv.save()
#             serializer = UserCVSectorSerializer(existing_cv)
#             return Response(serializer.data, status=200)
        
#         # Create a new CV upload
#         serializer = UserCVSectorSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             sector=Sector.objects.get(id=sector_id)
#             serializer.save(user=request.user, sector=sector)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCVSectorCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, sector_id):
        # Check if user already has a CV for this sector
        existing_cv = UserCVSector.objects.filter(
            user=request.user,
            sector_id=sector_id
        ).first()
        
        # Get the uploaded file
        cv_file = request.FILES.get('cv')
        if not cv_file:
            return Response({"error": "No CV file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Use the full filename with extension
        filename = cv_file.name
        
        if existing_cv:
            # Update the existing CV
            existing_cv.cv = cv_file
            existing_cv.file_name = filename  # Use the complete filename
            existing_cv.save()
            serializer = UserCVSectorSerializer(existing_cv)
            return Response(serializer.data, status=200)
        
        # Create a new CV upload
        try:
            sector = Sector.objects.get(id=sector_id)
            cv_sector = UserCVSector(
                user=request.user,
                sector=sector,
                cv=cv_file,
                filename=filename
            )
            cv_sector.save()
            serializer = UserCVSectorSerializer(cv_sector)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Sector.DoesNotExist:
            return Response({"error": "Sector not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

class UserCVSectorDetailAPIView(APIView):
    """
    API view for retrieving, updating, and deleting a single CV upload
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(UserCVSector, pk=pk, user=self.request.user)
    
    def get(self, request, pk):
        user_cv = self.get_object(pk)
        serializer = UserCVSectorSerializer(user_cv)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        user_cv = self.get_object(pk)
        user_cv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)