from django import forms
from .models import Paciente

class DocumentoForm(forms.ModelForm):
    """Formulario para el modelo Paciente."""
    class Meta:
        model = Paciente
        # Solo pedimos al usuario el nombre del paciente y el archivo original.
        fields = ['original',]
