from rest_framework import serializers
from ..models import Medico, Usuario 

class MedicoVerificarSerializer(serializers.ModelSerializer):
    

    usuario_verificado = serializers.BooleanField(required=True, write_only=True) 
    
    class Meta:
        model = Medico

        fields = ['medico_id', 'usuario_verificado'] 
        read_only_fields = ['medico_id']

    def update(self, instance, validated_data):
        """
        Actualiza el campo 'usuario_verificado' del objeto Usuario asociado al Medico.
        """

        try:
            usuario = instance.usuario_id 
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"error": "No se encontró el Usuario asociado a este Médico."})


        nuevo_estado = validated_data.pop('usuario_verificado', None)

        if nuevo_estado is not None:
            usuario.usuario_verificado = nuevo_estado
            usuario.save()


        return instance