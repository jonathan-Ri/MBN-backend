import random
import time
from django.core.cache import cache 
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings 
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Medico, Paciente, Usuario


# Tiempo de vida del código en segundos (ej: 5 minutos)
OTP_TIMEOUT = 300 

class SendOtpEmailView(APIView):
    """
    Genera un código OTP, lo guarda en caché y lo envía por email.
    """
    def post(self, request):
        email = request.data.get('email')

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Por seguridad, no reveles si el email existe o no
            return Response(
                {"detail": "Proceso de verificación iniciado."}, 
                status=status.HTTP_200_OK
            )

        # 1. Generar Código OTP (ej: 6 dígitos)
        otp_code = ''.join(random.choices('0123456789', k=6))
        
        # 2. Guardar el código en la caché de Django
        # La clave de caché debe ser única para el usuario.
        cache_key = f'otp_{user.usuario_id}'
        cache.set(cache_key, otp_code, timeout=OTP_TIMEOUT)

        # 3. Enviar el Email
        try:
            send_mail(
                'Tu Código de Verificación de un Solo Uso (OTP)',
                f'Tu código de verificación es: {otp_code}. Este código expira en 5 minutos.',
                settings.DEFAULT_FROM_EMAIL, # Remitente
                [user.email], # Destinatario
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error al enviar email: {e}")
            return Response(
                {"detail": "Error al enviar el código de verificación."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"detail": "Código de verificación enviado a tu email."}, 
            status=status.HTTP_200_OK
        )
    

    
class VerifyOtpEmailView(APIView):
    """
    Verifica el código OTP enviado por email.
    """
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        try:
            usuario = Usuario.objects.get(usuario_correo=email)
        except Usuario.DoesNotExist:
            return Response(
                {"detail": "Credenciales inválidas."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cache_key = f'otp_{usuario.usuario_id}'
        stored_otp = cache.get(cache_key)

        if stored_otp and stored_otp == otp_code:
            # 1. Éxito: El código es correcto. Eliminar de la caché.
            cache.delete(cache_key) 
            
            # -----------------------------------------------------------
            # 💡 PASO CRÍTICO: GENERAR TOKENS JWT Y DATA DEL USUARIO
            # -----------------------------------------------------------
            
            refresh = RefreshToken.for_user(usuario)
            
            # Reutiliza la lógica de obtener data específica del rol (Medico/Paciente)
            usuario_id_a_buscar = usuario.usuario_id 
            response_data = {}
            
            # Lógica para obtener el ID de Médico/Paciente (similar a tu LoginView original)
            if usuario.usuario_rol == "medico":
                try:
                    medico = Medico.objects.get(usuario_id=usuario_id_a_buscar)
                    rol_id = medico.medico_id
                except Medico.DoesNotExist:
                    rol_id = None
                rol_key = "medico_id"
            elif usuario.usuario_rol == "paciente":
                try:
                    paciente = Paciente.objects.get(usuario_id=usuario_id_a_buscar)
                    rol_id = paciente.paciente_id
                except Paciente.DoesNotExist:
                    rol_id = None
                rol_key = "paciente_id"
            elif usuario.usuario_rol == "admin":
                rol_id = None
                rol_key = None
            else:
                return Response({"error": "Rol de usuario no reconocido"}, status=status.HTTP_400_BAD_REQUEST)

            # Construir el objeto de datos de respuesta
            usuario_data = {
                "id": usuario.pk,
                "nombre": usuario.usuario_nombre,
                "correo": usuario.usuario_correo,
                "rol": usuario.usuario_rol,
                "usuario_verificado": usuario.usuario_verificado
            }
            if rol_key:
                usuario_data[rol_key] = rol_id
                
            response_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "usuario": usuario_data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # 3. Fallo: Código incorrecto o expirado
            return Response(
                {"detail": "Código inválido o expirado. Inténtalo de nuevo."}, 
                status=status.HTTP_400_BAD_REQUEST
            )