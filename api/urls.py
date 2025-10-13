# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.paciente_view import PacienteViewSet 
from api.views.usuario_view import UsuarioViewSet
from api.views.narrativa_escrita_view import NarrativaEscritaViewSet, NarrativasPorPacienteView
from api.views.register import RegisterView
from api.views.login_view import LoginView
from api.views.narraitiva_imagen_view import CrearNarrativaArchivoView
from api.views.medico_view import MedicoViewSet
from api.views.notificacion_view import NotificacionViewSet


router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'narrativas', NarrativaEscritaViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'notificacion', NotificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('narrativa-archivo/', CrearNarrativaArchivoView.as_view(), name='crear-narrativa-archivo'),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('narrativas/paciente/<int:paciente_id>/', NarrativasPorPacienteView.as_view(), name='narrativas-por-paciente'),
]

