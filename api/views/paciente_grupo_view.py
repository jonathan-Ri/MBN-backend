from rest_framework import viewsets
from ..models import PacienteGrupo
from ..serializers.paciente_grupo_serializer import PacienteGrupoSerializer

class PacienteGrupoViewSet(viewsets.ModelViewSet):
    queryset = PacienteGrupo.objects.all()
    serializer_class = PacienteGrupoSerializer
    def get_queryset(self):
        # 1. Obtener el queryset base
        queryset = PacienteGrupo.objects.all()
        
        # 2. Obtener los IDs de los parámetros de consulta (query parameters)
        paciente_id = self.request.query_params.get('paciente', None)
        grupo_colectivo_id = self.request.query_params.get('grupo_colectivo', None)
        
        # 3. Aplicar el filtro por Paciente ID
        if paciente_id is not None:
            # Filtra por el campo 'paciente' (clave foránea)
            # El valor debe ser un ID entero.
            queryset = queryset.filter(paciente_id=paciente_id)
            
        # 4. Aplicar el filtro por Grupo Colectivo ID
        if grupo_colectivo_id is not None:
            # Filtra por el campo 'grupo_colectivo' (clave foránea)
            # El valor debe ser un ID entero.
            queryset = queryset.filter(grupo_colectivo_id=grupo_colectivo_id)
            
        # 5. Devolver el queryset filtrado (o el queryset completo si no hay filtros)
        return queryset