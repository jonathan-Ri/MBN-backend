# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from ..models import Usuario
from rest_framework.permissions import AllowAny
from ..models import Medico, Paciente
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
        print("Usuario rol:", usuario.usuario_rol)
        response_data = {}

        if not check_password(contrasenia, usuario.usuario_contrasenia):
            return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)
        

        usuario_id_a_buscar = usuario.usuario_id 

        if usuario.usuario_rol == "medico":
            
            try:
                medico = Medico.objects.get(usuario_id=usuario_id_a_buscar)
            except Medico.DoesNotExist:
                # Maneja el caso en que no se encuentre ningún médico
                medico = None 
            if medico:
                usuario_data = {
                    "id": usuario.pk,
                    "nombre": usuario.usuario_nombre,
                    "correo": usuario.usuario_correo,
                    "rol": usuario.usuario_rol,
                    "medico_id": medico.medico_id,
                    "usuario_verificado":usuario.usuario_verificado
                }
                response_data = {
                    "usuario": usuario_data
                }
        elif usuario.usuario_rol == "paciente":

            print(usuario_id_a_buscar)
            try:
                # Filtra el modelo Medico donde el campo 'usuario_id' es igual al ID del usuario
                paciente = Paciente.objects.get(usuario_id=usuario_id_a_buscar)
            except Medico.DoesNotExist:
                # Maneja el caso en que no se encuentre ningún médico
                paciente = None 
            print("Paciente relacionado:", paciente)
            if paciente:
                usuario_data = {
                    "id": usuario.pk,
                    "nombre": usuario.usuario_nombre,
                    "correo": usuario.usuario_correo,
                    "rol": usuario.usuario_rol,
                    "paciente_id": paciente.paciente_id,
                    "usuario_verificado":usuario.usuario_verificado
                }
                response_data = {
                    "usuario": usuario_data
                }
                # Generar tokens JWT
        elif usuario.usuario_rol == "admin":
            usuario_data = {
                "id": usuario.pk,
                "nombre": usuario.usuario_nombre,
                "correo": usuario.usuario_correo,
                "rol": usuario.usuario_rol,
                "usuario_verificado":usuario.usuario_verificado
            }
            response_data = {
                "usuario": usuario_data
            }

  #      refresh = RefreshToken.for_user(usuario)
        else:
            return Response({"error": "Rol de usuario no reconocido"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data)
