
from django import forms
from django.db import models

from .models import Assignment
from django.core.exceptions import ValidationError

from apps.registration.models import Profile


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = [
            'publication',
            'referees',
            'article',
        ]

        widgets = {
            'article': forms.Select(),
        }

        labels = {
            'referees': 'Arbitros',
            'article': 'Artículo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # * máximo 4 asignaciones por arbitro y máximo 2 arbitros por artículo
        if self.instance.article.assignment.status == '1':

            # profiles = self.instance.article.profile.profiles.all()

            # print(profiles)
            # query = models.Q(type_user="2")

            # for profile in profiles:
            #     print(profile)
            #     query |= models.Q(profiles__in=[profile])

            # print(query, query)

            # * filtrar los arbitros que no tengan más de 4 asignaciones pendientes de manera individual
            self.fields['referees'].queryset = Profile.objects.filter(
                type_user="2",
                profiles__in=self.instance.article.profile.profiles.all()
            ).annotate(
                count_assignments=models.Subquery(
                    Assignment.objects.filter(
                        referees=models.OuterRef('pk'),
                        completed=False
                    ).values('referees').annotate(count_assignments=models.Count('referees')).values('count_assignments')
                )
            ).filter(
                count_assignments__lt=4
            ).distinct()
            
            # print(Profile.objects.filter(
            #     query
            # ).annotate(
            #     count_assignments=models.Subquery(
            #         Assignment.objects.filter(
            #             referees=models.OuterRef('pk'),
            #             completed=False
            #         ).values('referees').annotate(count_assignments=models.Count('referees')).values('count_assignments')
            #     )
            # ).filter(
            #     count_assignments__lt=4
            # ).distinct().query)

            # .distinct().annotate(
            #     count_assignments=models.Count(
            #         'assignments', filter=models.Q(assignments__completed=False))
            # ).filter(
            #     count_assignments__lte=6
            # )


        a = 1

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.referees.count() == 0:
            referees = cleaned_data.get('referees')

            if referees:
                if len(referees) > 2:
                    self.add_error(
                        'referees', 'No puede asignar más de 2 arbitros')
                elif len(referees) < 2:
                    self.add_error(
                        'referees', 'Debe asignar 2 arbitros')
        else:

            if 'referees' in self.changed_data:
                raise ValidationError(
                    'No puedes modificar los arbitros asignados')

        return cleaned_data

        # * show obj+
