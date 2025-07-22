# backend/urls.py (o el nombre de tu archivo principal de urls del proyecto)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Incluye las URLs de tu aplicaci\~on 'core'
    # Aseg\~urate de que 'core' est\~e en INSTALLED_APPS en settings.py
]