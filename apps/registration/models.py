from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.school.models import School

# Create your models here.


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    if not old_instance.avatar == 'avatars/default.jpg':
        old_instance.avatar.delete()

    return 'avatars/' + filename


# * Choices type user
TYPE_USER = (
    ('1', 'Autor'),
    ('2', 'Evaluador'),
)


class Profile(models.Model):
    avatar = models.ImageField(
        upload_to=custom_upload_to, blank=True, null=True, default='avatars/default.jpg')
    type_user = models.CharField(
        max_length=1, choices=TYPE_USER, verbose_name='Tipo de usuario')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuario', related_name='profile')
    # school = models.ForeignKey(
    #     School, on_delete=models.CASCADE, verbose_name='Escuela', null=True, blank=True)
    # first_join = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Actualizado en')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


# * Delete avatar when delete user
@receiver(models.signals.pre_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.avatar:
        if instance.avatar != 'avatars/default.jpg':
            instance.avatar.delete()
            print('delete avatar')


@receiver(models.signals.post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        profile = Profile.objects.get_or_create(user=instance)
        print("Profile created!")

