# api/serializers.py
from rest_framework import serializers
from ..models import NarrativaArchivo

class NarrativaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrativaArchivo
        fields = ['narrativa_archivo_id', 'paciente', 'narrativa_archivo_url', 'create_at', 'update_at']
        read_only_fields = ['create_at', 'update_at']  # la ruta se guarda automáticamente
