from rest_framework import serializers
from ..models import Paciente, Usuario

class PacienteSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(source='Usuario', read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='Usuario', write_only=True)
    class Meta:
        model = Paciente
        fields = '__all__'
        read_only_fields = ('Paciente_id',)
