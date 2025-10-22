from rest_framework import viewsets
from ..models import PacienteMedico
from ..serializers.pacienteMedico_serializer import PacienteMedicoSerializer

class PacienteMedicoViewSet(viewsets.ModelViewSet):
    queryset = PacienteMedico.objects.all() 
    serializer_class = PacienteMedicoSerializer

    def get_queryset(self):
        queryset = PacienteMedico.objects.all()
        
        medico_id_param = self.request.query_params.get('medico_id', None)

        if medico_id_param is not None:
            try:
                medico_id_a_filtrar = int(medico_id_param)
            except (ValueError, TypeError):
                medico_id_a_filtrar = None
            
            if medico_id_a_filtrar is not None:
                queryset = queryset.filter(medico_id=medico_id_a_filtrar)
                return queryset

        return queryset