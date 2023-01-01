from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models

# * django model utils
from model_utils.models import TimeStampedModel

# Create your models here.

# * custom upload to

def custom_upload_to(instance, filename):
    old_instance = Home.objects.get(pk=instance.pk)
    if not old_instance.image == 'home/itssmt.png':
        old_instance.image.delete()
    if not old_instance.brand_image == 'home/logo1.png':
        old_instance.brand_image.delete()

    return 'home/' + filename


# * home model


class Home(TimeStampedModel):
    title = models.CharField(max_length=100, verbose_name='Título')
    subtitle = models.CharField(max_length=100, verbose_name='Subtítulo')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(
        verbose_name='Imagen Principal', upload_to=custom_upload_to, default='home/itssmt.png')
    brand_image = models.ImageField(
        verbose_name='Imagen de marca', upload_to=custom_upload_to, default='home/logo1.png')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Página principal'
        verbose_name_plural = 'Página principal'


# * remove image file when object is deleted


@receiver(post_delete, sender=Home)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.brand_image.delete(False)

    
