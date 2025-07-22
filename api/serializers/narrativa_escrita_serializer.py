from rest_framework import serializers
from ..models import Paciente, NarrativaEscrita

class NarrativaEscritaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(source='Usuario', read_only=False)

    class Meta:
        model = NarrativaEscrita
        fields = '__all__'
        read_only_fields = ('Narrativa_id',)