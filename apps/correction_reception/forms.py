from django import forms
from .models import ArticleCorrection
from apps.article_review.models import Note


class CorrectionReceptionForm(forms.ModelForm):

    def get_article(self):
        return self.instance

    corrections = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label='Correcciones',
        required=True,
        help_text='Todas las correcciones deben ser seleccionadas'
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
