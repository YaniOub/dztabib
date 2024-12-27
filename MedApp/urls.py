from django.urls import path,include
from . import views
from rest_framework_nested import routers

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
]