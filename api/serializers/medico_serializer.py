from rest_framework import serializers
from ..models import Medico, Usuario, Notificacion
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
        read_only_fields = ('medico_id','usuario_id')


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
    
        medico = Medico.objects.create(usuario_id=usuario, **validated_data)
        try:
            if medico: # Solo crea si el médico existe

                buscar_medico= Usuario.objects.filter(usuario_rol="admin").values('usuario_id').first()
                print("entra al if")
                notificacion = Notificacion.objects.create(
                    usuario_id = 16, # buscar_medico # administrador de prueba, cambiar al desplegar
                    
                    # Campos fijos que deseas (ejemplo de bienvenida o registro)
                    notificacion_visto=0, #  0 = no visto
                    notificacion_estado='nueva', 
                    notificacion_contenido=f'Nuevo Medico Registrado. ID: {medico.medico_id}',
                    notificacion_tipo="registro_usuario_medico"                  
                )
                print(notificacion)
            else:
                print("no entra al if")
            
        except Exception as e:
            # Es importante loguear cualquier error en la creación de la notificación
            print(f"Error al crear notificación para el usuario {usuario.usuario_id}: {e}")
            # NOTA: No hacemos fallar la creación del Paciente si la notificación falla.


        
        return medico