from rest_framework import viewsets
from ..models import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer
from rest_framework.exceptions import NotFound # Para manejar 404

class UsuarioViewSet(viewsets.ModelViewSet):
    # Usamos ReadOnlyModelViewSet para solo permitir GET (list y retrieve)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    lookup_value_regex = '[^/]+'

    def get_object(self):
        """
        Sobrescribe get_object() para buscar el usuario usando
        el campo 'usuario_correo' proporcionado en la URL (self.kwargs['pk']).
        """
        # 1. Obtiene el valor de la URL (que por defecto se llama 'pk')
        correo_o_id = self.kwargs.get('pk')
        
        try:
            user = Usuario.objects.get(usuario_correo=correo_o_id)
            return user
            
        except Usuario.DoesNotExist:
            raise NotFound(detail=f"Usuario con correo/ID '{correo_o_id}' no encontrado.")