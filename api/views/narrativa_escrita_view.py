from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import NarrativaEscrita
from ..serializers.narrativa_escrita_serializer import NarrativaEscritaSerializer
from django.db.models import Q # Importamos Q para hacer búsquedas OR y AND complejos


class NarrativaEscritaViewSet(viewsets.ModelViewSet):
    queryset = NarrativaEscrita.objects.all()
    serializer_class = NarrativaEscritaSerializer

    def get_queryset(self):
        # 1. Base del Queryset
        queryset = NarrativaEscrita.objects.all()
        
        # 2. Obtener parámetros de consulta de la URL
        nombre_completo = self.request.query_params.get('nombre_completo', None)
        rut = self.request.query_params.get('rut', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)
        
        # -----------------------------------------------------------
        # A. FILTRO por Nombre Completo (Apellido Paterno y Materno + Nombre de Usuario)
        # -----------------------------------------------------------
        if nombre_completo:
            # Separamos el término de búsqueda por espacios para buscar coincidencias parciales
            terminos = nombre_completo.split()
            
            # Usamos un objeto Q vacío para construir las condiciones OR
            q_objects = Q()
            for term in terminos:
                # Búsqueda LIKE insensible a mayúsculas/minúsculas en el nombre y ambos apellidos
                q_objects |= Q(Paciente__paciente_apaterno__icontains=term)
                q_objects |= Q(Paciente__paciente_amaterno__icontains=term)
                q_objects |= Q(Paciente__usuario_id__usuario_nombre__icontains=term)

            queryset = queryset.filter(q_objects)
            
        # -----------------------------------------------------------
        # B. FILTRO por RUT de Paciente
        # -----------------------------------------------------------
        if rut:
            # Filtro por coincidencia parcial (LIKE) en el campo 'paciente_rut'
            queryset = queryset.filter(
                Paciente__paciente_rut__icontains=rut
            )
            
        # -----------------------------------------------------------
        # C. FILTRO por Rango de Fechas (Frame de Fecha de Creación)
        # -----------------------------------------------------------
        if fecha_inicio and fecha_fin:
            # __range de Django ORM busca entre los dos valores (inclusivo)
            queryset = queryset.filter(
                create_at__range=[fecha_inicio, fecha_fin]
            )
        elif fecha_inicio:
            # __gte (greater than or equal) para buscar desde la fecha de inicio
            queryset = queryset.filter(create_at__gte=fecha_inicio)
        elif fecha_fin:
            # __lte (less than or equal) para buscar hasta la fecha de fin
            queryset = queryset.filter(create_at__lte=fecha_fin)
            
        return queryset.distinct()

class NarrativasPorPacienteView(APIView):
    def get(self, request, paciente_id):
        narrativas = NarrativaEscrita.objects.filter(Paciente_id=paciente_id)
        serializer = NarrativaEscritaSerializer(narrativas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
