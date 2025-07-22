# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PacienteViewSet 
  
  # importa aquí las vistas necesarias
#C:\Users\elper\Desktop\App Medicina Narrativa\Backend\medicinaNarrativa\backend\api\views\paciente_view.py
router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)

urlpatterns = router.urls
