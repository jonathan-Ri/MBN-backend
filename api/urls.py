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
from api.views.pacienteMedico_view import PacienteMedicoViewSet
from api.views.grupo_colectivo_view import GrupoColectivoViewSet
from api.views.paciente_grupo_view import PacienteGrupoViewSet
#C:\Users\elper\Desktop\App Medicina Narrativa\Backend\medicinaNarrativa\backend\api\views\pacienteMedico_view.py

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'narrativas', NarrativaEscritaViewSet, basename='narrativa_escrita')
router.register(r'medicos', MedicoViewSet)
router.register(r'notificacion', NotificacionViewSet, basename='notificacion')
router.register(r'pacientemedicos', PacienteMedicoViewSet)
router.register(r'grupocolectivo', GrupoColectivoViewSet)
router.register(r'pacientegrupo', PacienteGrupoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('narrativa-archivo/', CrearNarrativaArchivoView.as_view(), name='crear-narrativa-archivo'),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('narrativas/paciente/<int:paciente_id>/', NarrativasPorPacienteView.as_view(), name='narrativas-por-paciente'),
]

