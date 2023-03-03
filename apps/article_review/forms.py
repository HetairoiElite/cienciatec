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
        
        widgets = {
            'comments': forms.Textarea(
                attrs=({
                    'placeholder': 'Comentarios',
                    'rows': 3,
                })
            )
        }


    def clean(self):
        cleaned_data = super().clean()

        comments = cleaned_data.get('comments')

        if len(comments) > 1000:
            self.add_error(
                'comments', 'El comentario no puede tener más de 1000 caracteres')

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

        widgets = {
            'line': forms.NumberInput(
                attrs=({
                    'placeholder': 'Línea',
                    'required': 'true'
                })
            ),
            'description': forms.Textarea(
                attrs=({
                    'placeholder': 'Nota',
                    'rows': 2,
                    'required': 'true'
                })
            )
        }
