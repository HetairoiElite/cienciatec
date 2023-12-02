
# * imports pythonfrom apps.proposal_reception.models import ArticleProposal

# * time
import time

# * imports django

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

# * receiver for signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel

# * apps
from core.models import Home
from .events import Event
from .managers import PublicationManager
from apps.proposal_reception.models import ArticleProposal
# * abstract class event


# * publicacion está compuesta por los siguientes eventos one to one
# * 1. Recepción de propuestas
# * 2. Revisión de articulos
# * 3. Envio de correcciones
# * 4. Recepción de correcciones
# * 5. Entrega  de dictamen final
# * 6. publicación de articulos


class Publication(Event):

    numero_publicacion = models.PositiveIntegerField(
        verbose_name='Numero de publicación',
        help_text='Numero de publicación',
        unique=True,
    )
    
    numero_folio = models.PositiveIntegerField(
        verbose_name='Número de oficio actual', default=1)
    # try:
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True, blank=True, related_name='publications',
                             default='2')
    # except:
    #     pass

    current = models.BooleanField(
        verbose_name='Publicación actual', help_text='Publicación actual', default=True)

    objects = PublicationManager()

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return 'Publicación #' + str(self.numero_publicacion)

    def check_overlap(self, start_date, end_date):

        try:
            # if self.start_date <= start_date <= self.end_date:
            if self.start_date <= start_date:

                return True
            # if self.start_date <= end_date <= self.end_date:
            if self.start_date <= end_date:
                return True
            # if start_date <= self.start_date <= end_date:
            if start_date <= self.start_date:
                return True
            # if start_date <= self.end_date <= end_date:
            if start_date <= self.end_date:
                return True
            return False
        except:

            # * detetime compare timezones django
            if timezone.localtime(self.start_date).date() <= start_date <= timezone.localtime(self.end_date).date():
                return True
            if timezone.localtime(self.start_date).date() <= end_date <= timezone.localtime(self.end_date).date():
                return True
            if start_date <= timezone.localtime(self.start_date).date() <= end_date:
                return True
            if start_date <= timezone.localtime(self.end_date).date() <= end_date:
                return True
            return False

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self)

    def clean(self):
        if self.end_date is not None:
            if self.end_date <= self.start_date:
                raise ValidationError(
                    'La fecha de finalizacion debe ser mayor a la fecha de inicio')

            events = Publication.objects.filter(
                start_date__lte=self.end_date, end_date__gte=self.start_date).exclude(id=self.id)

            if events.exists():
                raise ValidationError('El evento se cruza con otros eventos')
        else:
            if self.start_date <= timezone.now():
                raise ValidationError(
                    'La fecha de inicio debe ser mayor a la fecha actual')

            events = Publication.objects.filter(
                start_date__lte=self.start_date, end_date__gte=self.start_date + timezone.timedelta(days=36)).exclude(id=self.id)

            if events.exists():
                raise ValidationError('El evento se cruza con otros eventos')

        super().clean()

    def save(self):

        if self.current:
            Publication.objects.filter(current=True).update(current=False)

        if self.end_date is None:
            self.end_date = self.start_date + timezone.timedelta(days=36)

        super().save()

class Article(TimeStampedModel):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name='articles')
    article_proposal = models.OneToOneField(
        ArticleProposal, on_delete=models.CASCADE, related_name='article')
    file = models.FileField(verbose_name='Archivo', upload_to='articles/')
    fecha_publicacion = models.DateField(
        verbose_name='Fecha de publicación', null=True, blank=True)
    doi = models.CharField(verbose_name='DOI', max_length=100, null=True, blank=True,
                           help_text='Cada vez que se actualice este campo, se notificará al autor')
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

    def __str__(self):
        return self.article_proposal.title 

    def get_absolute_url(self):
        url = reverse('publications:article_detail', args=[self.id])
        
        return url
     
    
    def publicar(self):
        from dotenv import load_dotenv
        import os
        from docx import Document
        from core.functions import remove_line_numbering_from_docx
        
        load_dotenv()
        
        # * descargar correction file
        
        
        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.local':
            path = self.article_proposal.correction.correction_file.path
            from docx import Document
             
            document = Document(path)
            
            remove_line_numbering_from_docx(document)
            
            document.save(path)
             
            # * convert docx to pdf
            from docx2pdf import convert
            import pythoncom
            import shutil
            from django.conf import settings

            pythoncom.CoInitialize()

            # Eliminar el antiguo template en la carpeta de descargas
            try:
                os.remove(settings.BASE_DIR + '/downloads/correction_file.pdf')
            except:
                pass
             
            shutil.copy(self.article_proposal.correction.correction_file.path, settings.BASE_DIR / 'downloads' / 'correction_file.docx')
            
            convert(settings.BASE_DIR / 'downloads' / 'correction_file.docx', settings.BASE_DIR / 'downloads' / 'correction_file.pdf')
        else:
            import subprocess
            from django.core.files.storage import default_storage
            import os
            
            path = self.article_proposal.correction.correction_file.path
            
            with default_storage.open(path) as f:
                with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename('correction_file.docx')), 'wb') as d:
                    d.write(f.read())
                    
                doc = Document(settings.BASE_DIR / 'downloads' / 'correction_file.docx')
                
                remove_line_numbering_from_docx(doc)
                
                doc.save(settings.BASE_DIR / 'downloads' / 'correction_file.docx')
                    
                output = subprocess.check_output(('libreoffice', '--headless', '--convert-to', 'pdf',
                                                  settings.BASE_DIR / 'downloads' / 'correction_file.docx', '--outdir', settings.BASE_DIR / 'downloads'))
                    
        with open(settings.BASE_DIR / 'downloads'/ 'correction_file.pdf', 'rb') as f:
            from django.core.files import File
            self.file.save(f'{self.article_proposal.title}.pdf', File(f))
            
         
        self.save()
            
             
        
        
        
        self.fecha_publicacion = timezone.now()
        # * descargar correction file
         
        