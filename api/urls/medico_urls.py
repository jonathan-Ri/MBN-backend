from rest_framework.routers import DefaultRouter
from ..views import MedicoViewSet

router = DefaultRouter()
router.register(r'medico', MedicoViewSet)

urlpatterns = router.urls
