# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from ..models import Usuario
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    #usuario_correo
    #usuario_contrasenia
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get("usuario_correo")
        contrasenia = request.data.get("usuario_contrasenia")
        try:
            usuario = Usuario.objects.get(usuario_correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


        print("Password plano recibido:", contrasenia)
        print("Password en DB:", usuario.usuario_contrasenia)
        if not check_password(contrasenia, usuario.usuario_contrasenia):
            return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

  #      refresh = RefreshToken.for_user(usuario)
        return Response({
   #        "access": str(refresh.access_token),
      #     "refresh": str(refresh),
            "usuario": {
                "id": usuario.pk,
                "nombre": usuario.usuario_nombre,
                "correo": usuario.usuario_correo,
                "rol": usuario.usuario_rol,
            }
        })
