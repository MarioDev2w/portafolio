from rest_framework import serializers
from .models import Skill, Project, AuditFinding, ContactMessage

class SkillSerializer(serializers.ModelSerializer):
    # Campo extra para enviar a React el texto legible ("Blue Team & SIEM") además de la clave ("blue")
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Skill
        fields = [
            'id', 
            'name', 
            'category', 
            'category_display', 
            'proficiency', 
            'icon_name', 
            'description', 
            'is_featured'
        ]


class AuditFindingSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = AuditFinding
        fields = [
            'id', 
            'title', 
            'target_component', 
            'cvss_score', 
            'severity', 
            'severity_display', 
            'vulnerability_description', 
            'remediation_steps', 
            'is_sanitized'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    # NESTED SERIALIZER:
    # Gracias a related_name='findings' en el modelo AuditFinding, DRF incrusta
    # automáticamente la lista de hallazgos asociados dentro del JSON de cada proyecto.
    findings = AuditFindingSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'category_display',
            'summary',
            'problem_diagnosis',
            'architecture_description',
            'architecture_image',
            'log_evidence',
            'mitigation',
            'tools_used',
            'github_url',
            'pdf_report',
            'is_featured',
            'created_at',
            'findings'  # Lista anidada
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 
            'sender_name', 
            'sender_email', 
            'subject', 
            'message', 
            'is_encrypted_pgp', 
            'created_at'
        ]
        # Protegemos estos campos para que un cliente o atacante no intente modificarlos por HTTP
        read_only_fields = ['id', 'created_at', 'is_read']