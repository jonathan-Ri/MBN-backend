from rest_framework import serializers
from ..models import Paciente, Medico, Usuario # Asegúrate de importar tus modelos

# 🟢 SERIALIZER ANIDADO para Paciente
class PacienteDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        # Lista los campos específicos del paciente que quieres incluir
        fields = ['paciente_id', 'paciente_rut', 'paciente_apaterno', 'paciente_fecha_nacimiento'] 

# 🟢 SERIALIZER ANIDADO para Medico
class MedicoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        # Lista los campos específicos del médico que quieres incluir
        fields = ['medico_id', 'medico_especialidad', 'medico_colegiatura']