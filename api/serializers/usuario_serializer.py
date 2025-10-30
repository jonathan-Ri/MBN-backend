from ..models import Usuario
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UsuarioSerializer(serializers.ModelSerializer):
    usuario_contrasenia = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('create_at', 'update_at')


    def update(self, instance, validated_data):
        """
        Sobrescribe el método de actualización. 
        Si 'usuario_contrasenia' está presente en los datos, aplica el hash.
        """
        if 'usuario_contrasenia' in validated_data and 'usuario_rol' in validated_data:
            rol_usuario= validated_data.pop('usuario_rol')
            if rol_usuario == "admin":
                password_raw = validated_data.pop('usuario_contrasenia')
                hashed_password = make_password(password_raw)
                
                # 3. Asigna el hash al campo de la instancia
                instance.usuario_contrasenia = hashed_password
            else:
                raise serializers.ValidationError("Solo los usuarios con rol 'admin' pueden cambiar la contraseña.")
        
        # 4. Llama al método update original para manejar el resto de los campos
        return super().update(instance, validated_data)