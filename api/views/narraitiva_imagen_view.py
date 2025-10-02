from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.narrativa_archivo_serializer import NarrativaArchivoSerializer


class CrearNarrativaArchivoView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NarrativaArchivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # guarda el archivo y genera la ruta automáticamente
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)