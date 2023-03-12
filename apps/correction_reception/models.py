from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.


def custom_upload__to_correction(instance, filename):
    try:

        old_instance = ArticleCorrection.objects.get(pk=instance.pk)
        old_instance.correction_file.delete()
        return 'corrections/' + filename
    except:
        return 'corrections/' + filename


class ArticleCorrection(TimeStampedModel):
    correction_file = models.FileField(
        upload_to=custom_upload__to_correction, verbose_name='Plantilla corregida', null=True)

    article = models.OneToOneField(
        'Recepcion_Propuestas.ArticleProposal', on_delete=models.CASCADE, related_name='correction', verbose_name='Artículo', null=True, blank=True)

    class Meta:
        verbose_name = 'Corrección'
        verbose_name_plural = 'Correcciones'

    def __str__(self):
        return str(self.article)
