from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.school.models import School




def custom_upload_to(instance, filename):
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
        if not old_instance.avatar == 'avatars/default.jpg':
            old_instance.avatar.delete()

        return 'avatars/' + filename
    except:
        return 'avatars/' + filename


TYPE_USER = (
    ('1', 'Autor'),
    ('2', 'Arbitro'),
)


class Profile(models.Model):
    avatar = models.ImageField(
        upload_to=custom_upload_to, blank=True, null=True, default='avatars/default.jpg')
    type_user = models.CharField(
        max_length=1, choices=TYPE_USER, verbose_name='Tipo de usuario', null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuario', related_name='profile')

    profiles = models.ManyToManyField(
        'Asignacion_Arbitros.Profile', verbose_name='Perfiles de articulos', related_name='article_profiles', blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'



@receiver(models.signals.pre_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if instance.avatar != 'avatars/default.jpg':
            instance.avatar.delete()
            print('delete avatar')


@receiver(models.signals.post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        profile = Profile.objects.get_or_create(user=instance)
        print("Profile created!")
