
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

# * apps
from core.models import Home
from apps.reviewer_assignment.models import Assignment, ArticleProfile
from .events import Event
from .managers import PublicationManager
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
    # try:
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True, blank=True, related_name='publications',
                             default='1')
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

