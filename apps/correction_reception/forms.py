from django import forms
from .models import ArticleCorrection
from apps.article_review.models import Note, Review


class CorrectionReceptionForm(forms.ModelForm):

    def get_article(self):
        return self.instance

    corrections = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label='Observaciones',
        required=True,
        help_text='Todas las observaciones deben ser seleccionadas'
    )
    
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'required': 'true',
                                     'rows': '10',
                                     'placeholder': 'Comentarios',
                                     'readonly': 'true',
                                     'style': 'resize:none;'}),
        label='Comentarios',
        required=True,
        help_text='Comentarios de los árbitros que debes tener en cuenta para la corrección.'
    )

    class Meta:
        model = ArticleCorrection
        fields = ['correction_file']

        labels = {
            'correction_file': 'Plantilla corregida'
        }

        widgets = {
            'correction_file': forms.FileInput(attrs={'required': 'true',
                                                      # * docx
                                                      'accept': '.docx',
                                                      })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['corrections'].queryset = Note.objects.filter(
            review__assignment__article=self.instance.article)
        self.fields['corrections'].choices = [(note.pk, "Línea " + str(
            note.line) + ": " + note.description) for note in self.fields['corrections'].queryset]
        self.fields['corrections'].widget = forms.CheckboxSelectMultiple(
            attrs={'data-min-required':  Note.objects.filter(
                review__assignment__article=self.instance.article).count()
            },
            choices=self.fields['corrections'].choices
        )
        
        
        self.fields['comments'].initial = f'''
Arbitro 1: 
        {self.instance.article.assignment.reviews.all()[0].comments}
Arbitro 2:
        {self.instance.article.assignment.reviews.all()[1].comments}
        '''

class ReportForm(forms.Form):
    
    
    dictamen = forms.CharField()
         