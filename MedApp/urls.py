from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('doctor', views.DoctorViewSet)
router.register('patient', views.PatientViewSet)


urlpatterns = router.urls 