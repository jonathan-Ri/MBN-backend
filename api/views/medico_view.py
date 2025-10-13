from rest_framework import viewsets
from ..models import Medico
from ..serializers.medico_serializer  import MedicoSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer