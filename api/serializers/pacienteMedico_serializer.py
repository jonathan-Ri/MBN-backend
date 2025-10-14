from ..models import PacienteMedico
from rest_framework import serializers


class PacienteMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteMedico
        fields = '__all__' 
        read_only_fields = ('create_at', 'update_at')