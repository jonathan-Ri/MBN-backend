from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import NarrativaEscrita
from ..serializers.narrativa_escrita_serializer import NarrativaEscritaSerializer

class NarrativaEscritaViewSet(viewsets.ModelViewSet):
    queryset = NarrativaEscrita.objects.all()
    serializer_class = NarrativaEscritaSerializer
    
class NarrativasPorPacienteView(APIView):
    def get(self, request, paciente_id):
        narrativas = NarrativaEscrita.objects.filter(paciente_id=paciente_id)
        serializer = NarrativaEscritaSerializer(narrativas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
