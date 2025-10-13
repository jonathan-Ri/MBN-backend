from rest_framework import serializers
from ..models import Paciente, Usuario # Asegúrate de importar ambos

class PacienteVerificarSerializer(serializers.ModelSerializer):
    # ... (código del serializer dedicado)
    usuario_verificado = serializers.BooleanField(required=False, write_only=True) 
    
    class Meta:
        model = Paciente
        fields = ['paciente_id', 'usuario_verificado'] 
        read_only_fields = ['paciente_id']

    def update(self, instance, validated_data):
        # ... (lógica de actualización)
        usuario = instance.usuario_id 
        nuevo_estado = validated_data.get('usuario_verificado', True)
        usuario.usuario_verificado = nuevo_estado
        usuario.save()
        return instance