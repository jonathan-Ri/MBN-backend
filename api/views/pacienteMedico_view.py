from rest_framework import viewsets
from ..models import PacienteMedico
from ..serializers.pacienteMedico_serializer  import PacienteMedicoSerializer

class PacienteMedicoViewSet(viewsets.ModelViewSet):
    queryset = PacienteMedico.objects.all()
    serializer_class = PacienteMedicoSerializer