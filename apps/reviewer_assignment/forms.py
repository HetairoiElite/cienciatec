
from django import forms
from django.db import models

from .models import Assignment

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
        
        self.fields['referees'].queryset = Profile.objects.filter(
            type_user="2",
            profiles__in=self.instance.article.profile.profiles.all(),
        ).distinct().annotate(
            count_assignments=models.Count('assignments', filter=models.Q(assignments__completed=False))
        ).filter(
            count_assignments__lt=4
        )
        
        a = 1
            
    def clean(self):
        
        cleaned_data = super().clean()
        
        
        referees = cleaned_data.get('referees')
        
        # * máximo 4 asignaciones por arbitro y máximo 2 arbitros por artículo
        
        if referees:
            if len(referees) > 2:
                self.add_error('referees', 'No puede asignar más de 2 arbitros')
                
        return cleaned_data

        # * show obj
