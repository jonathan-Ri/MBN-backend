from rest_framework import viewsets
from ..models import Notificacion
from ..serializers.notificacion_serializer import NotificacionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        # 🟢 PASO 1: Permitir acceso completo para operaciones de detalle (DELETE/PUT/GET por ID)
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Notificacion.objects.all()
        
        # ----------------------------------------------------
        # 🟡 PASO 2: Lógica de Filtrado (Solo para la acción 'list')
        # ----------------------------------------------------
        user_id_param = self.request.query_params.get('usuario_id', None)
        user_id_a_filtrar = None

        if user_id_param:
             try:
                user_id_a_filtrar = int(user_id_param)
             except (ValueError, TypeError):
                 pass 

        if user_id_a_filtrar is not None:
             # Devolver solo las notificaciones para el usuario solicitado
             return Notificacion.objects.filter(usuario_id=user_id_a_filtrar)
        
        # 🔴 PASO 3: Si es 'list' y NO hay usuario, devolver vacío.
        return Notificacion.objects.none()