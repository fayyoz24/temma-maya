from django.urls import path
from .views import (
    SectorDetailAPIView, SectorListAPIView, 
    UserCVSectorListAPIView, UserCVSectorDetailAPIView,
    UserCVSectorCreateAPIView, 
)
urlpatterns = [
    path('sectors/', SectorListAPIView.as_view(), name='sector-list'),
    path('sectors/<int:sector_id>/', SectorDetailAPIView.as_view(), name='sector-detail'),
    path('user-cvs/', UserCVSectorListAPIView.as_view(), name='user-cv-list'),
    path('user-cvs/<int:pk>/', UserCVSectorDetailAPIView.as_view(), name='user-cv-detail'),
    path('user-cvs/create/<int:sector_id>/', UserCVSectorCreateAPIView.as_view(), name='user-cv-create'),
]