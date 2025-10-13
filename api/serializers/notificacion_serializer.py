from ..models import Notificacion
from rest_framework import serializers


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__' # Incluye todos los campos del modelo Usuario
        read_only_fields = ('create_at', 'update_at', 'notificacion_id')