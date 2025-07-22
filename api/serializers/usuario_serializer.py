from ..models import Usuario
from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('create_at', 'update_at')