from rest_framework import viewsets
from ..models import GrupoColectivo
from ..serializers.grupo_colectivo_serializer import GrupoColectivoSerializer

class GrupoColectivoViewSet(viewsets.ModelViewSet):
    queryset = GrupoColectivo.objects.all()
    serializer_class = GrupoColectivoSerializer