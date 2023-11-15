# * local imports
# * file

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
# * Email
from django.core.mail import EmailMessage

# * slugify
from django.utils.text import slugify

# * docxtpl
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm

# * django models utils
from model_utils.models import TimeStampedModel

from apps.events.events import Event
from core.models import Home
from apps.reviewer_assignment.models import Assignment, ArticleProfile

from .managers import ArticleProposalManager

# Create your models here.


# * custom upload to template user

def custom_upload_to_user_template(instance, filename):
    try:
        old_instance = ArticleProposal.objects.get(pk=instance.pk)
        old_instance.template.delete()
        return f'templates/{instance.author.user.username}/{filename}'
    except ArticleProposal.DoesNotExist:
        return f'templates/{instance.author.user.username}/{filename}'


def custom_upload_to_user_dictamen(instance, filename):
    try:
        old_instance = ArticleProposal.objects.get(pk=instance.pk)
        old_instance.dictamen.delete()
        return f'dictamen/{instance.author.user.username}/{filename}'
    except ArticleProposal.DoesNotExist:
        return f'dictamen/{instance.author.user.username}/{filename}'


def custom_upload_to_reception_letter(instance, filename):
    try:
        old_instance = ArticleProposal.objects.get(pk=instance.pk)
        old_instance.reception_letter.delete()
        return f'letters/{instance.author.user.username}/{filename}'
    except ArticleProposal.DoesNotExist:
        return f'letters/{instance.author.user.username}/{filename}'


def custom_upload_to_dictamen_letter(instance, filename):
    try:
        old_instance = ArticleProposal.objects.get(pk=instance.pk)
        old_instance.dictamen_letter.delete()
        return f'dictamenes/{instance.author.user.username}/{filename}'
    except ArticleProposal.DoesNotExist:
        return f'dictamenes/{instance.author.user.username}/{filename}'


def custom_upload_to_template_as_pdf(instance, filename):
    try:
        old_instance = ArticleProposal.objects.get(pk=instance.pk)
        old_instance.template_as_pdf.delete()
        return f'templates/{instance.author.user.username}/{filename}'
    except ArticleProposal.DoesNotExist:
        return f'templates/{instance.author.user.username}/{filename}'


class ArticleProposal(TimeStampedModel):

    objects = ArticleProposalManager.as_manager()

    publication = models.ForeignKey(
        'Eventos.Publication', on_delete=models.CASCADE, related_name='article_proposals',
        verbose_name='Publicación')

    title = models.CharField(
        max_length=100, verbose_name='Titulo', unique=True)

    slug = models.SlugField(
        max_length=200, verbose_name='Slug', unique=True, null=True, blank=True)

    author = models.ForeignKey(verbose_name='Autor', to='registration.Profile',
                               on_delete=models.CASCADE, related_name='article_proposal')

    MODALIDADES = (
        ('1', 'Investigación aplicada'),
        ('2', 'Investigación básica'),
        ('3', 'Divulgación'),
        ('4', 'Revisión (review)'),
        ('5', 'Ensayo'),
        ('6', 'Nota Científica'),
    )

    modality = models.CharField(
        max_length=1, choices=MODALIDADES, verbose_name='Modalidad', db_index=True)

    school = models.ForeignKey('Escuelas.School', on_delete=models.CASCADE,
                               related_name='article_proposals', verbose_name='Institución de adscripción', null=True, blank=True)

    new_school = models.CharField(
        max_length=100, verbose_name='Crédito de escuela', null=True, blank=True)

    template = models.FileField(
        verbose_name='Plantilla', upload_to=custom_upload_to_user_template)

    template_as_pdf = models.FileField(
        verbose_name='Plantilla en PDF', upload_to=custom_upload_to_template_as_pdf, null=True, blank=True)

   # * Keep icons in approved field

    # is_approved = models.BooleanField(
    #     null=True, verbose_name='Aprobado')

    # dictamen = models.FileField(
    #     verbose_name='Dictamen', upload_to=custom_upload_to_user_dictamen, null=True, blank=True)

    STATUS_CHOICES = (
        ('1', 'En espera'),
        ('2', 'Recibido'),
        ('3', 'En revisión'),
        ('4', 'Sin corregir'),
        ('5', 'Corregido'),
        ('6', 'En dictamen'),
        ('7', 'Aceptado'),
        ('8', 'Rechazado'),
        ('9', 'Publicado')
    )

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, verbose_name='Estatus', db_index=True, default='1')

    reception_letter = models.FileField(
        verbose_name='Carta de recepción', upload_to=custom_upload_to_reception_letter, null=True, blank=True, max_length=255)

    dictamen_letter = models.FileField(
        verbose_name='Carta de dictamen', upload_to=custom_upload_to_dictamen_letter, null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = 'Propuesta de artículo'
        verbose_name_plural = 'Propuestas de artículos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def generate_template_as_pdf(self):
        from dotenv import load_dotenv
        import os

        load_dotenv()

        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.local':
            from docx2pdf import convert
            import pythoncom
            import shutil

            pythoncom.CoInitialize()

            # * delete old template to downloads folder

            try:
                os.remove(settings.BASE_DIR / 'downloads' / 'template.docx')
            except:
                pass

            # * copy template to downloads folder
            shutil.copy(self.template.path, settings.BASE_DIR /
                        'downloads' / 'template.docx')

            convert(settings.BASE_DIR / 'downloads' / 'template.docx',
                    settings.BASE_DIR / 'downloads' / 'template.pdf')

        else:
            import subprocess
            from django.core.files.storage import default_storage
            
            path = self.template.path
            
            with default_storage.open(path) as f:
                with open(os.path.join(settings.BASE_DIR, 'downloads', os.path.basename('template.docx')), 'wb') as d:
                    d.write(f.read())

            output = subprocess.check_output(('libreoffice', '--headless', '--convert-to', 'pdf',
                                              settings.BASE_DIR / 'downloads' / 'template.docx',  '--outdir', settings.BASE_DIR / 'downloads'))

        with open(settings.BASE_DIR / 'downloads' / 'template.pdf', 'rb') as f:
            from django.core.files import File
            self.template_as_pdf.save(f'{self.title}.pdf',
                                      File(f))

        self.save()

    def send_reception_letter(self):
        
        reception_letter = Home.objects.first().reception_letters

        # * str basedir
        template_paths = (settings.BASE_DIR /
                          'downloads/Recepcion_de_articulo_EDIT.docx').__str__()

        print(template_paths)
        print(template_paths.__str__())

        doc = DocxTemplate(template_paths)

        seal = (settings.BASE_DIR / 'downloads/sello.jpg').__str__()

        firma_presidente = (settings.BASE_DIR /
                            'downloads/firma_presidente.png').__str__()
        firma_secretario = (settings.BASE_DIR /
                            'downloads/firma_secretary.png').__str__()

        sello = InlineImage(doc, image_descriptor=seal,
                            width=Cm(5.7), height=Cm(6.3))

        firma_presidente = InlineImage(
            doc, image_descriptor=firma_presidente, width=Cm(1.58), height=Cm(2.97)
        )

        firma_secretario = InlineImage(
            doc, image_descriptor=firma_secretario, width=Cm(3.63), height=Cm(2.58))

        context = {
            'fecha': timezone.now().strftime('%d de %B de %Y').replace(
                'January', 'Enero').replace(
                'February', 'Febrero').replace(
                'March', 'Marzo').replace(
                'April', 'Abril').replace(
                'May', 'Mayo').replace(
                'June', 'Junio').replace(
                'July', 'Julio').replace(
                'August', 'Agosto').replace(
                'September', 'Septiembre').replace(
                'October', 'Octubre').replace(
                'November', 'Noviembre').replace(
                'December', 'Diciembre'),
            'numero_oficio': reception_letter.current_number,
            'anio': timezone.now().year,
            'autor': self.author.user.first_name + ' ' + self.author.user.last_name,
            'titulo': self.title,
            'email': self.author.user.email,
            'coautores': self.coauthors.all(),
            'numero': Home.objects.first().publications.get_current().numero_publicacion,
            'firma_presidente': firma_presidente,
            'firma_secretary': firma_secretario,
            'PRESIDENT': reception_letter.president,
            'SECRETARY': reception_letter.secretary,
            'SEAL': sello,
        }

        doc.render(context)
        template_save = settings.BASE_DIR / f'downloads/Carta_de_recepcion.docx'
        doc.save(template_save)

        from dotenv import load_dotenv
        load_dotenv()
        import os

        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.local':

            from docx2pdf import convert
            import pythoncom

            pythoncom.CoInitialize()

            convert(settings.BASE_DIR / f'downloads/Carta_de_recepcion.docx',
                    settings.BASE_DIR / f'downloads/Carta_de_recepcion.pdf')

        else:
            import subprocess
            output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf', settings.BASE_DIR /
                                             'downloads/Carta_de_recepcion.docx', '--outdir', settings.BASE_DIR / 'downloads/'])
            print(output)

        with open(settings.BASE_DIR / 'downloads/Carta_de_recepcion.pdf', 'rb') as file:
            from django.core.files import File

            file = File(file)
            self.reception_letter.save(
                f'Carta_de_recepcion_{self.title}.pdf', file, save=True)

            email = EmailMessage(
                subject='Carta de recepción',
                body=f'Estimado {self.author.user.first_name} {self.author.user.last_name},\n\n'
                f'Adjunto se encuentra la carta de recepción de su propuesta de artículo "{self.title}"\n\n'
                f'Atentamente,\n'
                f'Comité Editorial de Ciencia y Tecnología',
                from_email='Jonathan90090@gmail.com',
                to=[self.author.user.email],
                reply_to=['jonathan90090@gmail.com'],
            )

            email.attach_file(settings.BASE_DIR /
                              'downloads/Carta_de_recepcion.pdf')

            email.send()

        self.save()

        reception_letter.current_number += 1
        reception_letter.save()
            
        

    def send_arbitration_report(self):
        report_letter = Home.objects.first().report_letters

        # * si el status es 7 (aceptado) se envía la carta de dictamen aprobación

        if self.status == '7':
            template_paths = (settings.BASE_DIR /
                              'downloads/DICTAMEN-APROBADO_edit.docx').__str__()
        elif self.status == '8':
            template_paths = (settings.BASE_DIR /
                              'downloads/DICTAMEN-NO-APROBADO_edit.docx').__str__()

        doc = DocxTemplate(template_paths)

        context = {
            'fecha': timezone.now().strftime('%d de %B de %Y').replace(
                'January', 'Enero').replace(
                'February', 'Febrero').replace(
                'March', 'Marzo').replace(
                'April', 'Abril').replace(
                'May', 'Mayo').replace(
                'June', 'Junio').replace(
                'July', 'Julio').replace(
                'August', 'Agosto').replace(
                'September', 'Septiembre').replace(
                'October', 'Octubre').replace(
                'November', 'Noviembre').replace(
                'December', 'Diciembre'),
            'presidente': report_letter.president,
            'autor': self.author.user.first_name + ' ' + self.author.user.last_name,
            'titulo': self.title,
            'numero': Home.objects.first().publications.get_current().numero_publicacion,
        }

        doc.render(context)
        template_save = settings.BASE_DIR / f'downloads/Carta_de_dictamen.docx'
        doc.save(template_save)

        from dotenv import load_dotenv
        load_dotenv()
        import os

        DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

        if DJANGO_SETTINGS_MODULE == 'cienciatec.settings.local':

            from docx2pdf import convert
            import pythoncom

            pythoncom.CoInitialize()

            convert(settings.BASE_DIR / f'downloads/Carta_de_dictamen.docx',
                    settings.BASE_DIR / f'downloads/Carta_de_dictamen.pdf')

        else:
            import subprocess
            output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf', settings.BASE_DIR /
                                             'downloads/Carta_de_dictamen.docx', '--outdir', settings.BASE_DIR / 'downloads/'])
            print(output)

        with open(settings.BASE_DIR / 'downloads/Carta_de_dictamen.pdf', 'rb') as file:

            from django.core.files import File

            file = File(file)
            self.dictamen_letter.save(
                f'Carta_de_dictamen_{self.title}.pdf', file)

            email = EmailMessage(
                subject='Carta de dictamen',
                body=f'Estimado {self.author.user.first_name} {self.author.user.last_name},\n\n'
                f'Adjunto se encuentra la carta de dictamen de su propuesta de artículo "{self.title}"\n\n'
                f'Atentamente,\n'
                f'Comité Editorial de Ciencia y Tecnología',
            )
            
            email.attach_file(settings.BASE_DIR / 'downloads/Carta_de_dictamen.pdf')
            
            email.send()
        
        self.save()
         


# * Imagenes de la propuesta
def custom_upload_to_user_images(instance, filename):
    try:
        old_instance = ArticleImage.objects.get(pk=instance.pk)
        old_instance.image.delete()
        return f'images/{instance.article_proposal.author.user.username}/{filename}'
    except ArticleImage.DoesNotExist:
        return f'images/{instance.article_proposal.author.user.username}/{filename}'


class ArticleImage(TimeStampedModel):

    article_proposal = models.ForeignKey(
        ArticleProposal, on_delete=models.CASCADE, related_name='proposal_images', verbose_name='Propuesta de artículo')
    image = models.ImageField(
        upload_to=custom_upload_to_user_images, verbose_name='Imagen')

    class Meta:
        verbose_name = 'Imagen del artículo'
        verbose_name_plural = 'Imagenes del artículo'

    def __str__(self):
        return self.image.name

# * Coautores de la propuesta


class Coauthor(TimeStampedModel):
    article_proposal = models.ForeignKey(
        ArticleProposal, on_delete=models.CASCADE, related_name='coauthors', verbose_name='Propuesta de artículo')
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre(s)', help_text='Máximo 2 nombres')
    apellido_paterno = models.CharField(
        max_length=100, verbose_name='Apellido paterno')
    apellido_materno = models.CharField(
        max_length=100, verbose_name='Apellido materno')
    email = models.EmailField(verbose_name='Correo electrónico')

    class Meta:
        verbose_name = 'Coautor'
        verbose_name_plural = 'Coautores'

    def __str__(self):
        return self.nombre + ' ' + self.apellido_paterno + ' ' + self.apellido_materno
