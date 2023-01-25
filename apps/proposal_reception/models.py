# * local imports
# * file

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

# * docxtpl
from docxtpl import DocxTemplate

# * django models utils
from model_utils.models import TimeStampedModel

from apps.events.events import Event

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


class ArticleProposal(TimeStampedModel):
    proposal_reception = models.ForeignKey(
        ProposalReception, on_delete=models.CASCADE, related_name='article_proposals', verbose_name='Recepción de propuestas')
    title = models.CharField(
        max_length=100, verbose_name='Titulo', help_text='Debe ser un titulo no muy largo')
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
        max_length=1, choices=MODALIDADES, verbose_name='Modalidad', help_text='Seleccione la modalidad de su artículo', db_index=True)

    school = models.ForeignKey('school.School', on_delete=models.CASCADE,
                               related_name='article_proposals', verbose_name='Institución de adscripción')
    template = models.FileField(
        verbose_name='Plantilla', upload_to=custom_upload_to_user_template)

   # * Keep icons in approved field

    is_approved = models.BooleanField(
        null=True, verbose_name='Aprobado')

    dictamen = models.FileField(
        verbose_name='Dictamen', upload_to=custom_upload_to_user_dictamen, null=True, blank=True)

    class Meta:
        verbose_name = 'Propuesta de artículo'
        verbose_name_plural = 'Propuestas de artículos'

    def __str__(self):
        return self.title

    def send_arbitration_report(self):
        print('send_arbitration_report')

        print(settings.MEDIA_ROOT + '/templates/arbitration_report.docx')

        if self.is_approved:
            doc = DocxTemplate(settings.MEDIA_ROOT +
                               '/home/DICTAMEN-APROBADO_edit.docx')
        else:
            doc = DocxTemplate(settings.MEDIA_ROOT +
                               '/home/DICTAMEN-NO-APROBADO_edit.docx')

        context = {
            'titulo': self.title,
            'autor': self.author.user.first_name + ' ' + self.author.user.last_name,
            'numero': self.proposal_reception.publication.numero_publicacion,
            # * now formato ejemplo: 6 de junio de 2021
            'fecha': timezone.now().strftime('%d de %B de %Y'),
        }

        print(context)

        doc.render(context)
        doc.save(settings.MEDIA_ROOT + '/home/dictamen.docx')

        # * docx2pdf
        from docx2pdf import convert

        import pythoncom

        pythoncom.CoInitialize()

        convert(settings.MEDIA_ROOT + '/home/dictamen.docx',
                settings.MEDIA_ROOT + '/home/dictamen.pdf')

        # * upload dictamen to dictamen field

        # * binary file
        with open(settings.MEDIA_ROOT + '/home/dictamen.pdf', 'rb') as f:

            from django.core.files import File

            file = File(f)

            self.dictamen.save('dictamen.pdf', file, save=True)

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
