# * local imports
# * file

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
# * slugify
from django.utils.text import slugify

# * docxtpl
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm

# * django models utils
from model_utils.models import TimeStampedModel

from apps.events.events import Event
from core.models import Home

# Create your models here.


class ProposalReception(Event):

    publication = models.OneToOneField(
        'events.Publication', on_delete=models.CASCADE, related_name='proposal_reception', verbose_name='Publicación')

    class Meta:
        verbose_name = 'Recepción de propuestas'
        verbose_name_plural = 'Recepción de propuestas'

    # * comprobar que la fecha de inicio de la recepción este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la recepción de propuestas debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Recepción de propuestas de la publicación #' + str(self.publication.numero_publicacion)


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


class ArticleProposal(TimeStampedModel):
    proposal_reception = models.ForeignKey(
        ProposalReception, on_delete=models.CASCADE, related_name='article_proposals', verbose_name='Recepción de propuestas')
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

    school = models.ForeignKey('school.School', on_delete=models.CASCADE,
                               related_name='article_proposals', verbose_name='Institución de adscripción', null=True, blank=True)

    new_school = models.CharField(
        max_length=100, verbose_name='Institución NO normalizada', null=True, blank=True)

    template = models.FileField(
        verbose_name='Plantilla', upload_to=custom_upload_to_user_template)

   # * Keep icons in approved field

    # is_approved = models.BooleanField(
    #     null=True, verbose_name='Aprobado')

    # dictamen = models.FileField(
    #     verbose_name='Dictamen', upload_to=custom_upload_to_user_dictamen, null=True, blank=True)

    STATUS_CHOICES = (
        ('1', 'En espera'),
        ('2', 'Recibido'),
    )

    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='Estatus', db_index=True, default='1')

    reception_letter = models.FileField(
        verbose_name='Carta de recepción', upload_to=custom_upload_to_reception_letter, null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = 'Propuesta de artículo'
        verbose_name_plural = 'Propuestas de artículos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)    
        
        super().save(*args, **kwargs)

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
        template_save = settings.BASE_DIR / f'letters/Carta_de_recepcion.docx'
        doc.save(template_save)

        from docx2pdf import convert
        import pythoncom

        pythoncom.CoInitialize()

        convert(settings.BASE_DIR / f'letters/Carta_de_recepcion.docx',
                settings.BASE_DIR / f'letters/Carta_de_recepcion.pdf')

        with open(settings.BASE_DIR / 'letters/Carta_de_recepcion.pdf', 'rb') as file:

            from django.core.files import File

            file = File(file)
            self.reception_letter.save(
                f'Carta_de_recepcion_{self.title}.pdf', file)

        self.save()

        reception_letter.current_number += 1
        reception_letter.save()

    # def send_reception_letter(self):

    # def send_arbitration_report(self):
    #     print('send_arbitration_report')

    #     print(settings.MEDIA_ROOT + '/templates/arbitration_report.docx')

    #     if self.is_approved:
    #         doc = DocxTemplate(settings.MEDIA_ROOT +
    #                            '/home/DICTAMEN-APROBADO_edit.docx')
    #     else:
    #         doc = DocxTemplate(settings.MEDIA_ROOT +
    #                            '/home/DICTAMEN-NO-APROBADO_edit.docx')

    #     context = {
    #         'titulo': self.title,
    #         'autor': self.author.user.first_name + ' ' + self.author.user.last_name,
    #         'numero': self.proposal_reception.publication.numero_publicacion,
    #         # * now formato ejemplo: 6 de junio de 2021
    #         'fecha': timezone.now().strftime('%d de %B de %Y'),
    #     }

    #     print(context)

    #     doc.render(context)
    #     doc.save(settings.MEDIA_ROOT + '/home/dictamen.docx')

    #     # * docx2pdf
    #     from docx2pdf import convert

    #     import pythoncom

    #     pythoncom.CoInitialize()

    #     convert(settings.MEDIA_ROOT + '/home/dictamen.docx',
    #             settings.MEDIA_ROOT + '/home/dictamen.pdf')

    #     # * upload dictamen to dictamen field

    #     # * binary file
    #     with open(settings.MEDIA_ROOT + '/home/dictamen.pdf', 'rb') as f:

    #         from django.core.files import File

    #         file = File(f)

    #         self.dictamen.save('dictamen.pdf', file, save=True)

        # self.save()


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
