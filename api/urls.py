from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, ProjectViewSet, AuditFindingViewSet, ContactMessageViewSet

# El DefaultRouter genera automáticamente las rutas estándar RESTful
router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'findings', AuditFindingViewSet)
router.register(r'contact', ContactMessageViewSet)

urlpatterns = [
    # Incluimos todas las rutas generadas por el router bajo el prefijo api/v1/
    path('', include(router.urls)),
]