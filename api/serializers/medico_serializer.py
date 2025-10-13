from rest_framework import serializers
from ..models import Medico, Usuario
from django.contrib.auth.hashers import make_password
from ..models import Usuario

# --- Serializer Anidado para el Usuario ---
class UsuarioNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Lista los campos del usuario que esperas en la consulta
        fields = ['usuario_nombre', 'usuario_correo', 'usuario_contrasenia', 'usuario_rol'] 
        
        # Oculta la contraseña en las respuestas y la marca para escritura.
        extra_kwargs = {'usuario_contrasenia': {'write_only': True}} 

class MedicoSerializer(serializers.ModelSerializer):

    usuario_data = UsuarioNestedSerializer(write_only=True)
    nombre_usuario = serializers.CharField(source='usuario_id.usuario_nombre', read_only=True)
    class Meta:
        model = Medico
        fields = ["nombre_usuario", "usuario_id","medico_id", "medico_apaterno", "medico_amaterno", "medico_rut", "medico_fecha_nacimiento", "medico_telefono", "medico_centro_atencion", "medico_genero","usuario_data"]
        read_only_fields = ('medico_id',)


    # 🚨 MÉTODO CORREGIDO: Debe estar INDENTADO dentro de la clase PacienteSerializer
    def create(self, validated_data):
        # 1. Extraer los datos anidados del usuario
        usuario_data = validated_data.pop('usuario_data')
        password_raw = usuario_data['usuario_contrasenia'] 
        hashed_password = make_password(password_raw)
        # 2. Crear el objeto Usuario con los datos extraídos
        #    RECOMENDACIÓN DE SEGURIDAD: Usa set_password() si Usuario es un modelo User.
        usuario = Usuario.objects.create(
            usuario_nombre=usuario_data['usuario_nombre'],
            usuario_correo=usuario_data['usuario_correo'],
            usuario_rol=usuario_data['usuario_rol'],
            # Esta línea guarda la contraseña en texto plano, lo cual NO es seguro.
            usuario_contrasenia=hashed_password
        )
        # Si usas set_password():
        # usuario.set_password(usuario_data['usuario_contrasenia'])
        # usuario.save()
        
        # 3. Crear el objeto Paciente, vinculándolo con el Usuario creado
        #    Asigna el objeto 'usuario' al campo ForeignKey 'usuario' del modelo Paciente
        medico = Medico.objects.create(usuario_id=usuario, **validated_data)
        
        return medico