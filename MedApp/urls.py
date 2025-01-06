from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, PatientViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'doctor', DoctorViewSet, basename='doctor')
router.register(r'patient', PatientViewSet, basename='patient')

# Include the router's URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Add all routes from the router
]