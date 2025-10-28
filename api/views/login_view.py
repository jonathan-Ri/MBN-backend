from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Usuario, Medico, Paciente
from .otp_mail_view import SendOtpEmailView, OTP_TIMEOUT, cache, random, send_mail, settings

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
            return Response({"error": "Correo no encontrado, verifique que el correo sea correcto,"}, status=status.HTTP_401_UNAUTHORIZED) # Mensaje genérico
        response_data = {}

        if not check_password(contrasenia, usuario.usuario_contrasenia):
            return Response({"error": "Contraseña incorrecta o cuenta no relacionada para la contraseña introducida"}, status=status.HTTP_401_UNAUTHORIZED)
        

        #usuario_id_a_buscar = usuario.usuario_id 

        # Generar Código OTP (ej: 6 dígitos)
        otp_code = ''.join(random.choices('0123456789', k=6))
        
        # Guardar el código en la caché
        cache_key = f'otp_{usuario.usuario_id}'
        cache.set(cache_key, otp_code, timeout=OTP_TIMEOUT)

       # Enviar el Email
        try:
            send_mail(
                'Tu Código de Verificación de un Solo Uso (2FA)',
                f'Tu código de verificación para iniciar sesión es: {otp_code}. Este código expira en 5 minutos.',
                settings.DEFAULT_FROM_EMAIL,
                [usuario.usuario_correo], # Usamos usuario.usuario_correo
                fail_silently=False,
            )
            # 💡 Respuesta al frontend: Indicar que el 2FA es requerido y el código fue enviado.
            return Response(
                {"detail": "Credenciales correctas. Se requiere código 2FA. Código enviado a tu correo.", 
                 "email": usuario.usuario_correo # Útil para el paso 2 del frontend
                }, 
                status=status.HTTP_202_ACCEPTED # 202 Accepted es un buen código para "proceso iniciado"
            )
        except Exception as e:
            # Manejar errores de correo electrónico (importante)
            print(f"Error al enviar email: {e}")
            return Response(
                {"error": "Error al enviar el código de verificación por correo."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
