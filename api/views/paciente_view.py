from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Paciente
from ..serializers.paciente_serializer import PacienteSerializer
from ..serializers.paciente_verificar_serializer import PacienteVerificarSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    
    @action(detail=True, methods=['patch'])

    def verificar_usuario(self, request, pk=None):
        # 1. Obtener el paciente
        paciente = self.get_object()
        
        # 2. Usar un serializer dedicado para la lógica de verificación
        serializer = PacienteVerificarSerializer(
            paciente, 
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            # El método update() de este serializer actualizará el Usuario
            serializer.save()
            return Response({'status': 'usuario verificado', 'usuario_id': paciente.usuario_id.usuario_id}, 
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)