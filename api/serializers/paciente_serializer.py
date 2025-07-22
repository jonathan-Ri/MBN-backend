from rest_framework import serializers
from ..models import Paciente, Usuario

class PacienteSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='Usuario.usuario_id', write_only=True)
    nombre_usuario = serializers.CharField(source='Usuario_id.Usuario_nombre', read_only=True)
    print("paciente nombre", nombre_usuario )
    class Meta:
        model = Paciente
        fields = '__all__'
        read_only_fields = ('paciente_id',)
