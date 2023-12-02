from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.
from django.conf import settings


def custom_upload__to_correction(instance, filename):
    try:

        old_instance = ArticleCorrection.objects.get(pk=instance.pk)
        old_instance.correction_file.delete()
        return 'corrections/' + filename
    except:
        return 'corrections/' + filename

def custom_upload__to_correction_as_pdf(instance, filename):
    try:

        old_instance = ArticleCorrection.objects.get(pk=instance.pk)
        old_instance.correction_file_as_pdf.delete()
        return 'corrections/' + filename
    except:
        return 'corrections/' + filename

def custom_upload__to_numbering_line(instance, filename):
    try:
        old_instance = ArticleCorrection.objects.get(pk=instance.pk)
        old_instance.numbering_line_file.delete()
        return 'corrections/' + filename
    except:
        return 'corrections/' + filename
    

class ArticleCorrection(TimeStampedModel):
    correction_file = models.FileField(
        upload_to=custom_upload__to_correction, verbose_name='Plantilla corregida', null=True, max_length=255)
    
    correction_file_as_pdf = models.FileField(
        upload_to=custom_upload__to_correction_as_pdf, verbose_name='Plantilla corregida en PDF', null=True, max_length=255)

    article = models.OneToOneField(
        'Recepcion_Propuestas.ArticleProposal', on_delete=models.CASCADE, related_name='correction', verbose_name='Artículo', null=True, blank=True)

    class Meta:
        verbose_name = 'Corrección'
        verbose_name_plural = 'Correcciones'

    def __str__(self):
        return str(self.article)
    
    # * correction file as pdf
    
        
    def generate_correction_file_as_pdf(self):
        from dotenv import load_dotenv
        import os
        from docx import Document
        from core.functions import add_line_numbering_to_docx

        load_dotenv()

        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.local':
            from docx2pdf import convert
            import pythoncom
            import shutil

            pythoncom.CoInitialize()

            # Eliminar el antiguo correction_file en la carpeta de descargas
            try:
                os.remove(settings.BASE_DIR / 'downloads' / 'correction_file.docx')
            except FileNotFoundError:
                pass

            # Copiar correction_file a la carpeta de descargas
            shutil.copy(self.correction_file.path, settings.BASE_DIR / 'downloads' / 'correction_file.docx')

            # Agregar numeración de líneas al correction_file
            doc = Document(settings.BASE_DIR / 'downloads' / 'correction_file.docx')
            add_line_numbering_to_docx(doc)
            doc.save(settings.BASE_DIR / 'downloads' / 'correction_file.docx')

            # Convertir el correction_file a PDF
            convert(settings.BASE_DIR / 'downloads' / 'correction_file.docx',
                    settings.BASE_DIR / 'downloads' / 'correction_file.pdf')

        else:
            import subprocess
            from django.core.files.storage import default_storage

            # Descargar el correction_file desde el almacenamiento predeterminado
            path = self.correction_file.path
            with default_storage.open(path) as f:
                with open(os.path.join(settings.BASE_DIR, 'downloads', 'correction_file.docx'), 'wb') as d:
                    d.write(f.read())

                # Agregar numeración de líneas al correction_file
                doc = Document(settings.BASE_DIR / 'downloads' / 'correction_file.docx')
                add_line_numbering_to_docx(doc)
                doc.save(settings.BASE_DIR / 'downloads' / 'correction_file.docx')

                # Convertir el correction_file a PDF utilizando LibreOffice
                output = subprocess.check_output(('libreoffice', '--headless', '--convert-to', 'pdf',
                                                settings.BASE_DIR / 'downloads' / 'correction_file.docx', '--outdir', settings.BASE_DIR / 'downloads'))

        # Guardar el PDF resultante en el modelo
        with open(settings.BASE_DIR / 'downloads' / 'correction_file.pdf', 'rb') as f:
            from django.core.files import File
            self.correction_file_as_pdf.save(f'{self.article.title}-corregido.pdf',
                                            File(f))

        # Guardar el modelo
        self.save()