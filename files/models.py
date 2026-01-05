from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Paciente(models.Model):
    """Modelo para representar un documento subido por un usuario."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='documentos')
    paciente = models.CharField(max_length=255)
    original = models.FileField(upload_to='files/original/')
    word = models.FileField(upload_to='files/word/', blank=True, null=True)
    pdf = models.FileField(upload_to='files/pdf/', blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paciente
