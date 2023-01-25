
# * imports python

from datetime import datetime, timedelta, date

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
from apps.proposal_reception.models import ProposalReception
from .events import Event, EventDay
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
        blank=True,
        null=True
    )
    # try:
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True, blank=True, related_name='publications',
                             default='1')
    # except:
    #     pass

    current = models.BooleanField(
        verbose_name='Publicación actual', help_text='Publicación actual', default=False)

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
            # * detetime compare timezones
            if datetime.date(self.start_date) <= start_date <= datetime.date(self.end_date):
                return True
            if datetime.date(self.start_date) <= end_date <= datetime.date(self.end_date):
                return True
            if start_date <= datetime.date(self.start_date) <= end_date:
                return True
            if start_date <= datetime.date(self.end_date) <= end_date:
                return True
            return False

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError(
                'La fecha de finalizacion debe ser mayor a la fecha de inicio')

        events = Publication.objects.filter(
            start_date__lte=self.end_date, end_date__gte=self.start_date).exclude(id=self.id)

        if events.exists():
            raise ValidationError('El evento se cruza con otros eventos')

        # * revisar que no exista otra publicación actual
        if self.current:
            other = Publication.objects.filter(
                current=True).exclude(id=self.id)
            if other.exists():
                raise ValidationError(
                    'Ya existe una publicación actual: (' + str(other.first()) + ')')

        # * no puede durar menos de 36 dias
        # if (self.end_date - self.start_date).days < 36:
        #     raise ValidationError('La publicación debe durar al menos 36 días')


# * 1. Recepción de propuestas


# * 2. Asignación de revisores


class ReviewerAssignment(Event):
    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='reviewer_assignment')

    class Meta:
        verbose_name = 'Asignación de revisores'
        verbose_name_plural = 'Asignación de revisores'

    # * comprobar que la fecha de inicio de la asignación de revisores este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la asignación de revisores debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Asignación de revisores de la publicación #' + str(self.publication.numero_publicacion)

# * 3. Revisión de articulos


class ArticleReview(Event):

    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='article_review')

    class Meta:
        verbose_name = 'Revisión de articulos'
        verbose_name_plural = 'Revisión de articulos'

    # * comprobar que la fecha de inicio de la revisión este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la revisión de articulos debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Revisión de articulos de la publicación #' + str(self.publication.numero_publicacion)

# * 4. Envio de correcciones


class CorrectionsSending(Event):

    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='corrections_sending')

    class Meta:
        verbose_name = 'Envio de correcciones'
        verbose_name_plural = 'Envio de correcciones'

    # * comprobar que la fecha de inicio del envio de correcciones este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio del envio de correcciones debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Envio de correcciones de la publicación #' + str(self.publication.numero_publicacion)

# * 5. Recepción de correccion de articulos


class CorrectionsReception(Event):

    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='corrections_reception')

    class Meta:
        verbose_name = 'Recepción de correccion de articulos'
        verbose_name_plural = 'Recepción de correccion de articulos'

    # * comprobar que la fecha de inicio de la recepción de correcciones este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la recepción de correcciones debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Recepción de correcciones de la publicación #' + str(self.publication.numero_publicacion)

    def __add__(self, other):
        return self + other

# * 6. Entrega  de dictamen final


class FinalReportSending(EventDay):

    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='final_report_sending')

    class Meta:
        verbose_name = 'Entrega  de dictamen final'
        verbose_name_plural = 'Entrega  de dictamen final'

    # * comprobar que la fecha de inicio de la entrega de dictamen final este
    # * dentro del rango de la publicación

    def check_overlap(self, day):
        # * checar si la fecha esta dentro del rango de la publicación
        exists = Publication.objects.filter(
            start_date__lte=day, end_date__gte=day).exists()

        return exists

    def clean(self):
        # if not self.check_overlap(self.day):
        #     raise ValidationError(
        #         'La fecha de entrega de dictamen final debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Entrega  de dictamen final de la publicación #' + str(self.publication.numero_publicacion)

# * 7. publicación de articulos


class ArticlePublication(EventDay):

    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name='article_publication')

    class Meta:
        verbose_name = 'Publicación de articulos'
        verbose_name_plural = 'Publicación de articulos'

    # * comprobar que la fecha de inicio de la publicación de articulos este
    # * dentro del rango de la publicación

    def check_overlap(self, day):
        # * checar si la fecha esta dentro del rango de la publicación
        exists = Publication.objects.filter(
            start_date__lte=day, end_date__gte=day).exists()

        return exists

    def clean(self):
        #     if not self.check_overlap(self.day):
        #         raise ValidationError(
        #             'La fecha de publicación de articulos debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Publicación de articulos de la publicación #' + str(self.publication.numero_publicacion)

# * cuando se crea una publicación se crean los eventos de la publicación


@receiver(post_save, sender=Publication)
def create_events(sender, instance, created, **kwargs):

    if created:
        # * colocar la fecha de inicio de la recepción de propuestas en la fecha de inicio de la publicación
        # * y la fecha de fin de la recepción de propuestas 10 días después de la fecha de inicio de la publicación

        ProposalReception.objects.create(
            publication=instance, start_date=instance.start_date, end_date=instance.start_date + timedelta(days=9))

        # * colocar la fecha de inicio de la asignación de revisores en la fecha de fin de la asignación de revisores
        # * y la fecha de fin de la asignación de revisores 3 días después de la fecha de fin de la recepción de propuestas

        ReviewerAssignment.objects.create(publication=instance, start_date=instance.proposal_reception.end_date,
                                          end_date=instance.proposal_reception.end_date + timedelta(days=3))

        # * colocar la fecha de inicio de la revisión de articulos en la fecha de fin de la asignación de revisores
        # * y la fecha de fin de la revisión de articulos 6 días después de la fecha de fin de la asignación de revisores

        ArticleReview.objects.create(publication=instance, start_date=instance.reviewer_assignment.end_date,
                                     end_date=instance.reviewer_assignment.end_date + timedelta(days=6))

        # * colocar la fecha de inicio del envio de correcciones en la fecha de fin de la revisión de articulos
        # * y la fecha de fin del envio de correcciones 2 días después de la fecha de inicio del envio de correcciones

        CorrectionsSending.objects.create(publication=instance, start_date=instance.article_review.end_date + timedelta(days=1),
                                          end_date=instance.article_review.end_date + timedelta(days=3))

        # * colocar la fecha de inicio de la recepción de correcciones en la fecha de fin del envio de correcciones
        # * y la fecha de fin de la recepción de correcciones 2 días después de la fecha de inicio de la recepción de correcciones

        CorrectionsReception.objects.create(publication=instance, start_date=instance.corrections_sending.end_date,
                                            end_date=instance.corrections_sending.end_date + timedelta(days=2))

        # * colocar el dia de la entrega de dictamen final 4 días después de la fecha de fin de la recepción de correcciones

        FinalReportSending.objects.create(
            publication=instance, day=instance.corrections_reception.end_date +
            timedelta(days=4)
        )

        # * colocar el dia de la publicación de articulos 8 días después de la fecha de fin de la recepción de correcciones

        ArticlePublication.objects.create(
            publication=instance, day=instance.final_report_sending.day +
            timedelta(days=9)
        )
    else:
        if instance.end_date != instance.article_publication.day:
            instance.proposal_reception.start_date = instance.start_date
            instance.proposal_reception.end_date = instance.start_date + \
                timedelta(days=9)
            instance.proposal_reception.save()

            instance.reviewer_assignment.start_date = instance.proposal_reception.end_date
            instance.reviewer_assignment.end_date = instance.proposal_reception.end_date + \
                timedelta(days=3)
            instance.reviewer_assignment.save()

            instance.article_review.start_date = instance.reviewer_assignment.end_date
            instance.article_review.end_date = instance.reviewer_assignment.end_date + \
                timedelta(days=6)
            instance.article_review.save()

            instance.corrections_sending.start_date = instance.article_review.end_date + \
                timedelta(days=1)
            instance.corrections_sending.end_date = instance.article_review.end_date + \
                timedelta(days=3)
            instance.corrections_sending.save()

            instance.corrections_reception.start_date = instance.corrections_sending.end_date
            instance.corrections_reception.end_date = instance.corrections_sending.end_date + \
                timedelta(days=2)
            instance.corrections_reception.save()

            instance.final_report_sending.day = instance.corrections_reception.end_date + \
                timedelta(days=4)
            instance.final_report_sending.save()

            instance.article_publication.day = instance.final_report_sending.day + \
                timedelta(days=9)
            instance.article_publication.save()

            instance.end_date = instance.article_publication.day
            instance.save()


# * cuando se actualiza un evento de la publicación se actualizan los eventos de la publicación
