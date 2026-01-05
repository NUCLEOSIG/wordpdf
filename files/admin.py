from django.contrib import admin
from .models import Paciente

# Register your models here.
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """Configuración del modelo Paciente en el panel de administración."""
    list_display = ('paciente', 'usuario', 'fecha_subida', 'original')
    list_filter = ('usuario', 'fecha_subida')
    search_fields = ('paciente', 'usuario__username')
    readonly_fields = ('fecha_subida',)
    ordering = ('-fecha_subida',)
