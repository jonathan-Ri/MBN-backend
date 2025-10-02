from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import Usuario
from django.db import IntegrityError


class RegisterView(APIView):
    def post(self, request):
        try:
            password_raw = request.data.get("usuario_contrasenia")
            hashed_password = make_password(password_raw)
            print(hashed_password)
            usuario = Usuario.objects.create(
                usuario_nombre=request.data.get("usuario_nombre"),
                usuario_correo=request.data.get("usuario_correo"),
                usuario_contrasenia=hashed_password,
                usuario_rol=request.data.get("usuario_rol")
            )
            return Response({"message": "Usuario creado correctamente", "id": usuario.usuario_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)