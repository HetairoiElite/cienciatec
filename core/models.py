from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models

# * mark safe
from django.utils.safestring import mark_safe

# * django model utils
from model_utils.models import TimeStampedModel

# * locals
from .managers import HomeManager

# Create your models here.


# * custom upload to


def custom_upload_to_image(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.image.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename


def custom_upload_to_brand(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.brand_image.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename


def custom_upload_to_favicon(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.favicon.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename


def custom_upload_to_convocatoria(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.convocatoria.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename


def custom_upload_to_acept_template(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.acept_template.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename


def custom_upload_to_reject_template(instance, filename):
    try:
        old_instance = Home.objects.get(pk=instance.pk)
        old_instance.reject_template.delete()
        return 'home/'+filename
    except Home.DoesNotExist:
        return 'home/'+filename

# * home model


class Home(TimeStampedModel):
    title = models.CharField(max_length=100, verbose_name='Título')
    subtitle = models.CharField(max_length=100, verbose_name='Subtítulo')

    image = models.ImageField(
        verbose_name='Imagen Principal', upload_to=custom_upload_to_image, null=True, blank=True)
    brand_image = models.ImageField(
        verbose_name='Imagen de marca', upload_to=custom_upload_to_brand,
        null=True, blank=True)

    favicon = models.ImageField(
        verbose_name='Favicon', upload_to=custom_upload_to_favicon,
        null=True, blank=True)

    description = models.TextField(verbose_name='Descripción')

    # * pdf de la convocatoria

    convocatoria = models.FileField(
        verbose_name='Convocatoria', upload_to=custom_upload_to_convocatoria,
        null=True, blank=True)

    acept_template = models.FileField(
        verbose_name='Plantilla de aceptación', upload_to=custom_upload_to_acept_template,
        null=True, blank=True)

    reject_template = models.FileField(
        verbose_name='Plantilla de no aceptación', upload_to=custom_upload_to_reject_template,
        null=True, blank=True)

    objects = HomeManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Página principal'
        verbose_name_plural = 'Página principal'

    def image_previewc(self):
        return mark_safe('<img src="%s" width="100px" />' % self.image.url)


# * remove image file when object is deleted


@receiver(post_delete, sender=Home)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.brand_image.delete(False)
    instance.favicon.delete(False)


# * Plantillas de articulos

# * custom upload to for article template

def custom_upload_to_article_template(instance, filename):
    try:
        old_instance = ArticleTemplate.objects.get(pk=instance.pk)
        old_instance.template.delete()
        return 'article_template/'+filename
    except ArticleTemplate.DoesNotExist:
        return 'article_template/'+filename


class ArticleTemplate(TimeStampedModel):
    home = models.ForeignKey(Home, on_delete=models.CASCADE,
                             verbose_name='Página principal', default=1, related_name='article_templates')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    template = models.FileField(
        verbose_name='Plantilla', upload_to=custom_upload_to_article_template, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Plantilla de artículo'
        verbose_name_plural = 'Plantillas de artículos'


def custom_upload_to_reception_letter(instance, filename):
    try:
        old_instance = ReceptionLetter.objects.get(pk=instance.pk)
        old_instance.template.delete()
        return 'home/'+filename
    except ReceptionLetter.DoesNotExist:
        return 'home/'+filename


def custom_upload_firm_pre(instance, filename):
    try:
        old_instance = ReceptionLetter.objects.get(pk=instance.pk)
        old_instance.president_firm.delete()
        return 'home/'+filename
    except ReceptionLetter.DoesNotExist:
        return 'home/'+filename


def custom_upload_firm_sec(instance, filename):
    try:
        old_instance = ReceptionLetter.objects.get(pk=instance.pk)
        old_instance.secretary_firm.delete()
        return 'home/'+filename
    except ReceptionLetter.DoesNotExist:
        return 'home/'+filename


def custom_upload_seal(instance, filename):
    try:
        old_instance = ReceptionLetter.objects.get(pk=instance.pk)
        old_instance.seal.delete()
        return 'home/'+filename
    except ReceptionLetter.DoesNotExist:
        return 'home/'+filename
    
def custom_upload_template_reception_letter(instance, filename):
    try:
        old_instance = ReceptionLetter.objects.get(pk=instance.pk)
        old_instance.template.delete()
        return 'home/'+filename
    except ReceptionLetter.DoesNotExist:
        return 'home/'+filename


class ReceptionLetter(TimeStampedModel):
    home = models.OneToOneField(Home, on_delete=models.CASCADE,
                                verbose_name='Página principal', default=1, related_name='reception_letters')
    # name = models.CharField(max_length=100, verbose_name='Nombre')
    template = models.FileField(
        verbose_name='Plantilla', upload_to= custom_upload_template_reception_letter, null=True, blank=True)

    # * número de oficio actual

    current_number = models.PositiveIntegerField(
        verbose_name='Número de oficio actual', default=1)

    # * presidente del comité de arbitraje

    president = models.CharField(
        max_length=100, verbose_name='Presidente del comité de arbitraje')

    president_firm = models.ImageField(
        verbose_name='Firma del presidente', upload_to=custom_upload_firm_pre,
        null=True, blank=True)

    # * secretario del comité de arbitraje

    secretary = models.CharField(
        max_length=100, verbose_name='Secretario del comité de arbitraje')

    secretary_firm = models.ImageField(
        verbose_name='Firma del secretario', upload_to=custom_upload_firm_sec,
        null=True, blank=True)

    # * sello del departamento de investigación

    seal = models.ImageField(
        verbose_name='Sello del departamento de investigación', upload_to=custom_upload_seal,
        null=True, blank=True)

    def __str__(self):
        return self.home.title

    class Meta:
        verbose_name = 'Carta de recepción'
        verbose_name_plural = 'Cartas de recepción'
