from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('blue', 'Blue Team & SIEM'),
        ('red', 'Pentesting & Offensive'),
        ('grc', 'GRC & ISO 27001'),
        ('hardware', 'Hardware & IoT'),
        ('devsec', 'DevSecOps & Scripting'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(
        default=80,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Porcentaje de dominio (1-100)"
    )
    icon_name = models.CharField(max_length=50, blank=True, help_text="Nombre del icono en Lucide o FontAwesome")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('SOC', 'SOC & Telemetría'),
        ('PENTEST', 'Web Pentesting'),
        ('HARDWARE', 'IoT & Hardware Sec'),
        ('GRC', 'GRC & Riesgo ISO 27001'),
        ('DFIR', 'Forense & Incidentes'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    summary = models.TextField(help_text="Resumen corto para la tarjeta principal")
    
    # Detalle en profundidad (Estudio de caso)
    problem_diagnosis = models.TextField(help_text="Diagnóstico o escenario inicial")
    architecture_description = models.TextField(help_text="Descripción de la solución / Topología")
    architecture_image = models.ImageField(upload_to='projects/architecture/', blank=True, null=True)
    
    # Evidencias y Mitigación
    log_evidence = models.TextField(blank=True, help_text="Comandos, logs o salidas sanitizadas")
    mitigation = models.TextField(help_text="Solución, parches o controles recomendados")
    
    # Metadatos
    tools_used = models.JSONField(default=list, help_text="Lista de herramientas, ej: ['Wazuh', 'pfSense', 'Suricata']")
    github_url = models.URLField(blank=True, null=True)
    pdf_report = models.FileField(upload_to='projects/reports/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AuditFinding(models.Model):
    SEVERITY_CHOICES = [
        ('CRITICAL', 'Crítico'),
        ('HIGH', 'Alto'),
        ('MEDIUM', 'Medio'),
        ('LOW', 'Bajo'),
    ]

    title = models.CharField(max_length=200)
    target_component = models.CharField(max_length=150, help_text="Ej: Portal Cautivo / API Endpoint")
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, help_text="Ejemplo: 8.5")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    vulnerability_description = models.TextField()
    remediation_steps = models.TextField()
    is_sanitized = models.BooleanField(default=True, help_text="Confirma que se eliminaron datos reales de clientes")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='findings', null=True, blank=True)

    def __str__(self):
        return f"[{self.severity}] {self.title} (CVSS {self.cvss_score})"


class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_encrypted_pgp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Mensaje de {self.sender_name} - {self.subject}"

# Create your models here.
