from rest_framework import viewsets
from ..models import Medico
from ..serializers.medico_serializer  import MedicoSerializer
from ..serializers.medico_verificar_serializer import MedicoVerificarSerializer
from rest_framework.decorators import action
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    @action(detail=True, methods=['patch'], serializer_class=MedicoVerificarSerializer)
    def verificar(self, request, pk=None):
        medico_instance = self.get_object()
        serializer = self.get_serializer(medico_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # Devolver los datos del médico actualizado o un mensaje de éxito
            return Response({'status': 'Usuario verificado/desverificado exitosamente.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)