
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

            from django.db.models import Count, OuterRef, Subquery, IntegerField
            from django.db.models.functions import Coalesce

            # Subconsulta interna para contar las asignaciones no completadas por cada árbitro
            count_assignments_subquery = Assignment.objects.filter(
                referees=OuterRef('pk'),
                completed=False
            ).values('referees').annotate(count_assignments=Count('referees')).values('count_assignments')

            # Subconsulta externa para obtener perfiles con la subconsulta interna calculada
            referees = Profile.objects.filter(
                type_user="2",
                profiles__in=self.instance.article.profiles.all()
            ).annotate(count_assignments=Coalesce(Subquery(count_assignments_subquery, output_field=IntegerField()), 0))

            # Aplicar el filtro y mostrar los resultados
            filtered_referees = referees.filter(count_assignments__lt=4).distinct()

    
            if filtered_referees.count() >= 2:
                self.fields['referees'].queryset = filtered_referees
            else:
                all_referees = Profile.objects.filter(type_user="2").annotate(
                    count_assignments=Coalesce(Subquery(count_assignments_subquery, output_field=IntegerField()), 0)
                )
                
                all_referees_filtered = all_referees.filter(count_assignments__lt=4, user__is_active=True).distinct()
                
                self.fields['referees'].queryset = all_referees_filtered
                
                if all_referees_filtered.count() < 2:
                    # * agregar un error en el text_help color rojo
                    from django.utils.safestring import mark_safe
                    self.fields['referees'].help_text += mark_safe(
                        '<br><span style="color:red">No hay suficientes arbitros disponibles</span>')
                    self.fields['referees'].widget.attrs['disabled'] = True
            
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
