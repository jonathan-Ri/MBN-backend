# core/serializers.py
from rest_framework import serializers
from .models import Usuario, Paciente, Medico, GrupoColectivo, PacienteMedico, PacienteGrupo, NarrativaEscrita, NarrativaArchivo, Notificacion, Administrador

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('create_at', 'update_at') # Campos que no se pueden modificar directamente via API

# Serializador para el modelo Paciente
# Incluye el serializador de Usuario para mostrar los datos del usuario asociado
class PacienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source='Usuario', write_only=True
    )

    class Meta:
        model = Paciente
        fields = [
            'Paciente_id', 'usuario', 'usuario_id', 'Paciente_rut',
            'Paciente_apaterno', 'Paciente_amaterno', 'Paciente_genero',
            'Paciente_fecha_nacimiento'
        ]
        read_only_fields = ('Paciente_id',)

# Serializador para el modelo Medico
class MedicoSerializer(serializers.ModelSerializer):
    Usuario = UsuarioSerializer(read_only=True)
    Usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source='Usuario', write_only=True
    )

    class Meta:
        model = Medico
        fields = '__all__'
        read_only_fields = ('Medico_id',)

# Serializador para el modelo GrupoColectivo
class GrupoColectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoColectivo
        fields = '__all__'
        read_only_fields = ('Grupo_colectivo_id', 'create_at', 'update_at')

# Serializador para la tabla intermedia PacienteMedico
class PacienteMedicoSerializer(serializers.ModelSerializer):
    Paciente = PacienteSerializer(read_only=True)
    Medico = MedicoSerializer(read_only=True)
    Paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='Paciente', write_only=True)
    Medico_id = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all(), source='Medico', write_only=True)

    class Meta:
        model = PacienteMedico
        fields = '__all__'
        read_only_fields = ('Paciente_Medico_id', 'create_at', 'update_at')

# Serializador para la tabla intermedia PacienteGrupo
class PacienteGrupoSerializer(serializers.ModelSerializer):
    Paciente = PacienteSerializer(read_only=True)
    Grupo_colectivo = GrupoColectivoSerializer(read_only=True)
    Paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='Paciente', write_only=True)
    Grupo_colectivo_id = serializers.PrimaryKeyRelatedField(queryset=GrupoColectivo.objects.all(), source='Grupo_colectivo', write_only=True)

    class Meta:
        model = PacienteGrupo
        fields = '__all__'
        read_only_fields = ('Paciente_Grupo_id', 'create_at', 'update_at')

# Serializador para NarrativaEscrita
class NarrativaEscritaSerializer(serializers.ModelSerializer):
    Paciente = PacienteSerializer(read_only=True)
    Paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='Paciente', write_only=True)

    class Meta:
        model = NarrativaEscrita
        fields = '__all__'
        read_only_fields = ('Narrativa_id', 'create_at', 'update_at')

# Serializador para NarrativaArchivo
class NarrativaArchivoSerializer(serializers.ModelSerializer):
    Paciente = PacienteSerializer(read_only=True)
    Paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='Paciente', write_only=True)

    class Meta:
        model = NarrativaArchivo
        fields = '__all__'
        read_only_fields = ('Narrativa_archivo_id', 'create_at', 'update_at')

# Serializador para Notificacion
class NotificacionSerializer(serializers.ModelSerializer):
    Usuario = UsuarioSerializer(read_only=True)
    Usuario_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='Usuario', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Notificacion
        fields = '__all__'
        read_only_fields = ('notificacion_id', 'create_at', 'update_at')

# Serializador para Administrador
class AdministradorSerializer(serializers.ModelSerializer):
    Usuario = UsuarioSerializer(read_only=True)
    Usuario_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='Usuario', write_only=True)

    class Meta:
        model = Administrador
        fields = '__all__'
        read_only_fields = ('Administrador_id',)
