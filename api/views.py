from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Skill, Project, AuditFinding, ContactMessage
from .serializers import (
    SkillSerializer, 
    ProjectSerializer, 
    AuditFindingSerializer, 
    ContactMessageSerializer
)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo permite peticiones GET (listar todas o ver una específica).
    Bloquea automáticamente POST, PUT, PATCH y DELETE.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exponemos los proyectos en modo solo lectura.
    Cambiamos el lookup_field a 'slug' para que las URLs sean profesionales.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'  # Permite buscar por URL: /api/v1/projects/auditoria-wazuh/


class AuditFindingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditFinding.objects.all()
    serializer_class = AuditFindingSerializer


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Al heredar SOLO de CreateModelMixin, este endpoint bloquea las peticiones GET.
    Nadie podrá listar ni leer tus mensajes, solo podrán enviar (POST).
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]