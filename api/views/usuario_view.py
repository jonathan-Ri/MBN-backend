from rest_framework import viewsets
from ..models import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    # Usamos ReadOnlyModelViewSet para solo permitir GET (list y retrieve)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer