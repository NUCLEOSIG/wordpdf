from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from django.contrib import messages
from .forms import DocumentoForm
from .models import Paciente

from django.conf import settings
from spire.doc import *
from spire.doc.common import *


# Create your views here.

def subir_documento(request):
    if request.method == 'POST':
        # Pasamos request.FILES para manejar la subida de archivos
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            # Creamos una instancia del modelo pero no la guardamos aún
            documento = form.save(commit=False)
            
            # Asignamos el usuario actual
            #documento.usuario = request.user

            # Extraer el nombre del archivo para usarlo como nombre del paciente
            uploaded_file = request.FILES['original']
            # Usamos os.path.splitext para quitar la extensión de forma segura
            documento.paciente = os.path.splitext(uploaded_file.name)[0]

            # Ahora sí, guardamos el objeto completo en la base de datos
            documento.save()
            messages.success(request, '¡Documento subido y procesado con éxito!')
            wordpdf(documento)
            # Redirigir a una nueva URL (puedes cambiar 'index' por la que prefieras)
            datos = Paciente.objects.all().order_by('-fecha_subida')[:50]
            return redirect('subir_documento') 
    else:
        form = DocumentoForm()
    pacientes = Paciente.objects.all().order_by('-fecha_subida')[:50]
    return render(request, 'subir_documento.html', {'form': form, 'pacientes': pacientes})


def lista_pacientes(request):
    """Muestra una lista de todos los pacientes/documentos subidos."""
    pacientes = Paciente.objects.all().order_by('-fecha_subida')[:150]
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})


def wordpdf(paciente_instance):
    """
    Procesa un archivo de Word, le añade una marca de agua y lo guarda como
    Word y PDF, actualizando la instancia del Paciente.
    """
    # Obtener el nombre base del archivo sin espacios
    file_name_base = os.path.splitext(os.path.basename(paciente_instance.original.name))[0].replace(" ", "_")
    
    # Rutas de entrada y salida usando os.path.join para compatibilidad
    input_file = paciente_instance.original.path
    watermark_image = os.path.join(settings.STATIC_ROOT, 'images', 'fondofirma.jpg')
    
    output_word_path = os.path.join(settings.MEDIA_ROOT, 'files', 'word', f"final-{file_name_base}.docx")
    output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'files', 'pdf', f"final-{file_name_base}.pdf")

    # Asegurarse de que los directorios de salida existan
    os.makedirs(os.path.dirname(output_word_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    # Crear un nuevo documento
    document = Document()
    document.LoadFromFile(input_file)

    # Agregar un renglón al principio del documento
    if document.Sections.Count > 0:
        # Insertar un párrafo vacío al principio del cuerpo de la primera sección
        paragraph = document.Sections.get_Item(0).Body.AddParagraph()
        document.Sections.get_Item(0).Body.ChildObjects.Insert(0, paragraph)

    # Cambiar el tamaño de la página a Carta para cada sección del documento
    for i in range(document.Sections.Count):
        section = document.Sections.get_Item(i)
        section.PageSetup.PageSize = PageSize.Letter()

        # Establecer los márgenes a 1 cm (1 cm = 28.35 puntos)
        margin_in_points = 28.35
        section.PageSetup.Margins.Left = margin_in_points
        section.PageSetup.Margins.Right = margin_in_points

        # Insertar la marca de agua en el encabezado para tener control total
        header = section.HeadersFooters.Header
        paragraph = header.AddParagraph()
        paragraph.Format.HorizontalAlignment = HorizontalAlignment.Left
        
        # Añadir la imagen al párrafo
        picture = paragraph.AppendPicture(watermark_image)
        
        # Posicionar la imagen en la esquina superior izquierda
        picture.HorizontalPosition = -30.0
        picture.VerticalPosition = -35.0
        picture.TextWrappingStyle = TextWrappingStyle.Behind
        picture.IsWashout = False

    # Guardar los documentos procesados
    document.SaveToFile(output_word_path, FileFormat.Docx)
    document.SaveToFile(output_pdf_path, FileFormat.PDF)
    document.Close()

    # Actualizar la instancia del paciente con las rutas de los nuevos archivos
    paciente_instance.word.name = os.path.join('files', 'word', f"final-{file_name_base}.docx")
    paciente_instance.pdf.name = os.path.join('files', 'pdf', f"final-{file_name_base}.pdf")
    paciente_instance.save(update_fields=['word', 'pdf'])