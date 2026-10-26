from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Skill, Project, AuditFinding, ContactMessage

# Registros simples
admin.site.register(Skill)
admin.site.register(AuditFinding)
admin.site.register(ContactMessage)

# Registro avanzado para Proyecto (autocompleta el slug automáticamente al escribir el título)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'summary', 'problem_diagnosis')