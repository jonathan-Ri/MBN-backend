from rest_framework import serializers
from ..models import Paciente, NarrativaEscrita

class NarrativaEscritaSerializer(serializers.ModelSerializer):
    
    # 🟢 Campo para mostrar el nombre del usuario/paciente (Lectura)
    # Asumo que la relación es Paciente -> Usuario -> usuario_nombre
    nombre_paciente = serializers.CharField(
        source='Paciente.usuario_id.usuario_nombre',  # Reemplaza 'usuario_id' y 'usuario_nombre' según tus modelos
        read_only=True
    )

    class Meta:
        model = NarrativaEscrita
        # Es mejor listar los campos explícitamente que usar '__all__'
        fields = [
            'narrativa_id', 
            'Paciente', # Clave foránea para la escritura (ID)
            'narrativa_escrita_contenido', # El campo que guardará el Rich Text
            'create_at', 
            'update_at',
            'nombre_paciente' # Campo de lectura
        ]
        # El campo `narrativa_id` es la clave primaria, es mejor dejarlo solo.
        read_only_fields = ('narrativa_id',)