from ..models import GrupoColectivo
from rest_framework import serializers


class GrupoColectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoColectivo
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('grupo_colectivo_id',)