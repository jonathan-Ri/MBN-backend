# views.py (donde defines GetAdminId)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Usuario 

class GetAdminId(APIView):
    def get(self, request):
        try:
            admin_id = Usuario.objects.filter(usuario_rol='admin').values_list('usuario_id', flat=True).first()
            
            if admin_id is not None:
                # 💡 CORRECCIÓN 1: Devuelve un objeto Response con el ID
                #return Response({'usuario_id': admin_id}, status=status.HTTP_200_OK)#en caso de produccion real
                return Response({'usuario_id': 16}, status=status.HTTP_200_OK)#admin de prueba
            else:
                # 💡 CORRECCIÓN 2: Devuelve un objeto Response con un error 404
                print("Advertencia: No se encontró ningún usuario con usuario_rol='admin'.")
                return Response(
                    {'detail': 'No se encontró ningún administrador.'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            print(f"Error al intentar obtener el ID del administrador: {e}")
            # 💡 CORRECCIÓN 3: Devuelve un objeto Response con un error 500
            return Response(
                {'detail': 'Error interno al procesar la solicitud.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )