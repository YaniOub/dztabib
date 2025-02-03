<<<<<<< HEAD

from django.urls import path,include
from . import views
from rest_framework_nested import routers
from .views import DoctorListView
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, PatientViewSet

router = routers.DefaultRouter()
router.register('doctor', views.DoctorViewSet)
router.register('patient', views.PatientViewSet)
router.register('appointment', views.AppointmentViewSet)

doctors_router = routers.NestedDefaultRouter(router, 'doctor', lookup='doctor')
doctors_router.register('appointments', views.AppointmentViewSet, basename='doctor-appointments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(doctors_router.urls)),
    path('appointment/create/<int:doctor_pk>/', views.AppointmentViewSet.as_view({'post': 'create'}), name='appointment-create'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),]  # Endpoint for listing doctors

=======
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
>>>>>>> d19a22425fa049f8d31040f4a022846ab5195744
