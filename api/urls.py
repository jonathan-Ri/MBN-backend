# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.paciente_view import PacienteViewSet 
from api.views.usuario_view import UsuarioViewSet
from api.views.narrativa_escrita_view import NarrativaEscritaViewSet, NarrativasPorPacienteView

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'narrativas', NarrativaEscritaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('narrativas/paciente/<int:paciente_id>/', NarrativasPorPacienteView.as_view(), name='narrativas-por-paciente'),
]
