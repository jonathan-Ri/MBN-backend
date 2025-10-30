# En tu archivo views.py (o api/auth_views.py)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password # 💡 Importación clave
from django.core.mail import send_mail
from ..models import Usuario # Importa tu modelo Usuario


def send_reset_password_email(user, token, uid):
    # NOTA: Debes cambiar 'TU_DOMINIO.com' por la URL de tu frontend web o app
    # que manejará la confirmación del token.
    reset_url = f"https://TU_DOMINIO.com/reset-password-confirm/{uid}/{token}/"
    
    mail_subject = "Restablece tu Contraseña"
    message = render_to_string('email_reset_password.html', { # Necesitas esta plantilla
        'user': user,
        'reset_url': reset_url,
    })
    
    try:
        send_mail(mail_subject, message, 'TU_CORREO@ejemplo.com', [user.usuario_correo])
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    
    try:
        user = Usuario.objects.get(usuario_correo=email)
    except Usuario.DoesNotExist:
        # ... (respuesta segura)
        return Response({"detail": "Si la cuenta existe, se ha enviado un email."}, status=status.HTTP_200_OK)
    
    # Parche 1: last_login
    if not hasattr(user, 'last_login'):
        user.last_login = None

    if not hasattr(user, 'get_email_field_name'):
        user.get_email_field_name = lambda: 'usuario_correo'

    if not hasattr(user, 'get_session_auth_hash'):
        user.get_session_auth_hash = lambda: user.usuario_contrasenia

    if not hasattr(user, 'password'):
        user.password = user.usuario_contrasenia


    # 1. Generar UID y Token (Ahora debería funcionar)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # 2. Enviar el correo
    success = send_reset_password_email(user, token, uid)

    if success:
        return Response(
            {"detail": "Email de restablecimiento enviado exitosamente."}, 
            status=status.HTTP_200_OK
        )
    else:
        # Error interno en el servidor de correos
        return Response(
            {"detail": "Error al enviar el email."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# NOTA: Necesitarás otro endpoint para manejar la confirmación del token (password_reset_confirm)
# que reciba el token, uid y la nueva contraseña.

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Endpoint para confirmar el token de restablecimiento y establecer la nueva contraseña.
    Recibe: {"uid": "base64encodedid", "token": "generatedtoken", "new_password": "micontrasenia"}
    """
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    # 1. Validaciones básicas de entrada
    if not all([uidb64, token, new_password]):
        return Response(
            {"detail": "Los campos 'uid', 'token' y 'new_password' son obligatorios."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # Aquí puedes añadir validaciones de seguridad de la contraseña (longitud, complejidad, etc.)
    if len(new_password) < 8:
        return Response(
            {"detail": "La contraseña debe tener al menos 8 caracteres."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Decodificar UID y obtener el usuario
    try:
        # Decodificar el uidb64 para obtener el ID del usuario (pk)
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    # 3. Verificar el Token
    if user is not None and default_token_generator.check_token(user, token):
        # El token es válido: hashear y guardar la nueva contraseña
        
        # 💡 Uso de make_password (Tu implementación actual)
        user.usuario_contrasenia = make_password(new_password)
        user.save()
        
        return Response(
            {"detail": "Contraseña restablecida exitosamente."}, 
            status=status.HTTP_200_OK
        )
    else:
        # El token es inválido o ha expirado
        return Response(
            {"detail": "El enlace de restablecimiento es inválido o ha expirado."}, 
            status=status.HTTP_400_BAD_REQUEST
        )