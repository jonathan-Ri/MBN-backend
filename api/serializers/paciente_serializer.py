from rest_framework import serializers
from ..models import Paciente, Usuario, Notificacion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

# --- Serializer Anidado para el Usuario ---
class UsuarioNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Lista los campos del usuario que esperas en la consulta
        fields = ['usuario_nombre', 'usuario_correo', 'usuario_contrasenia', 'usuario_rol'] 
        
        # Oculta la contraseña en las respuestas y la marca para escritura.
        extra_kwargs = {'usuario_contrasenia': {'write_only': True}} 

# --- Serializer Principal del Paciente ---
class PacienteSerializer(serializers.ModelSerializer):
    
    usuario_data = UsuarioNestedSerializer(write_only=True)
    nombre_usuario = serializers.CharField(source='usuario_id.usuario_nombre', read_only=True)
    medico_recomendado = serializers.IntegerField(write_only=True, required=False)
    # 🚨 Se eliminó el print() - no es válido en el cuerpo de la clase
    
    class Meta:
        model = Paciente
        fields = ['paciente_id', 
            'paciente_rut', 
            'paciente_apaterno',
            'paciente_amaterno',
            'paciente_genero',
            'paciente_fecha_nacimiento',
            'usuario_data',
            'nombre_usuario',
            'medico_recomendado'  
            ]
        read_only_fields = ('paciente_id',)
    
    def create(self, validated_data):
        # 1. Extraer los datos anidados del usuario
        usuario_data = validated_data.pop('usuario_data')
        medico_recomendado = validated_data.pop('medico_recomendado')
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
        paciente = Paciente.objects.create(usuario_id=usuario, **validated_data)
        print(medico_recomendado)



        try:
            if paciente: # Solo crea si el médico existe
                notificacion = Notificacion.objects.create(
                    usuario_id = medico_recomendado, 
                    
                    # Campos fijos que deseas (ejemplo de bienvenida o registro)
                    notificacion_visto=0, #  0 = no visto
                    notificacion_estado='nueva', # Asumo que este campo existe y es un CharField
                    notificacion_contenido=f'Nuevo paciente registrado. ID: {paciente.paciente_id}',
                    notificacion_tipo="registro_usuario"                  
                )
                print(notificacion)
                print(usuario_data['medico_recomendado'])
        except Exception as e:
            # Es importante loguear cualquier error en la creación de la notificación
            print(f"Error al crear notificación para el usuario {usuario.usuario_id}: {e}")
            # NOTA: No hacemos fallar la creación del Paciente si la notificación falla.
        
        return paciente
    
