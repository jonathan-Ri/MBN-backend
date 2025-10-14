from rest_framework import viewsets
from ..models import Notificacion
from ..serializers.notificacion_serializer import NotificacionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    def get_queryset(self):
        user_id_param = self.request.query_params.get('usuario_id', None)
        if user_id_param == None:
            print("es nulo")
        else:
            print(user_id_param)
        # 2. Convertir a entero de forma segura
        try:
            # Si el parámetro es una cadena como '12', se convierte a 12.
            # Si el parámetro es una cadena como 'null', 'undefined', o 'abc', fallará.
            user_id_a_filtrar = int(user_id_param)
        except (ValueError, TypeError):
            # Si falla la conversión (es None, 'null', 'undefined', o no es un número)
            # asumimos que el ID no es válido para filtrar.
            user_id_a_filtrar = None
        print(user_id_a_filtrar)
        
        if user_id_a_filtrar is not None:
            # ✅ Filtrar solo si user_id_a_filtrar es un entero válido (el ID del usuario)
            return Notificacion.objects.filter(usuario_id=user_id_a_filtrar)
        
        # ❌ Si el ID no es válido o no se proporcionó, no debe devolver todas las notificaciones
        # con usuario_id=null, sino un conjunto vacío (por seguridad)
        return Notificacion.objects.none() 