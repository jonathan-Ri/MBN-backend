from ..models import PacienteGrupo
from rest_framework import serializers


class PacienteGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteGrupo
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('paciente_grupo_id',)