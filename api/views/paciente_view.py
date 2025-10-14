from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Paciente
from ..serializers.paciente_serializer import PacienteSerializer
from ..serializers.paciente_verificar_serializer import PacienteVerificarSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_queryset(self):
        queryset = Paciente.objects.all()
        medico_id = self.request.query_params.get('medico_id')
        
        if medico_id is not None:
            queryset = queryset.filter(pacientemedico__medico_id=medico_id).distinct()   
        return queryset.order_by('paciente_apaterno') 
    
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
    

    @action(detail=True, methods=['get'])
    def obtener_usuario_id(self, request, pk=None):
        """
        Ruta: GET /api/pacientes/{pk}/obtener_usuario_id/
        Devuelve el ID del usuario asociado al paciente.
        """
        try:
            # 1. Obtener el objeto Paciente usando el PK proporcionado
            paciente = self.get_object()
            
            # 2. Acceder al campo de relación y obtener el ID
            usuario_id = paciente.usuario_id.usuario_id
            
            # 3. Retornar solo el ID
            return Response({'usuario_id': usuario_id}, status=status.HTTP_200_OK)
            
        except Paciente.DoesNotExist:
            return Response(
                {'detail': 'Paciente no encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Manejar cualquier otro error (ej. relación usuario_id nula)
            return Response(
                {'detail': f'Error al obtener el ID de usuario: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )