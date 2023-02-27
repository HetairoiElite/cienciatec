from django import forms

from .models import *


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'comments',
        ]

        labels = {
            'comments': 'Comentarios',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comments'].widget.attrs['rows'] = 10

    def clean(self):
        cleaned_data = super().clean()

        comments = cleaned_data.get('comments')

        if len(comments) > 1000:
            self.add_error('comments', 'El comentario no puede tener más de 1000 caracteres')

    def save(self, commit=True):
        review = super().save(commit=False)
        review.save()
        return review
    
class NotesForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
            'description',
            'line'
        ]

        labels = {
            'description': 'Nota',
            'line': 'Línea',
        }