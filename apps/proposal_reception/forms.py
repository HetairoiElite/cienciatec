
from django import forms

from .models import ArticleProposal, Coauthor, ArticleImage
from apps.school.models import School

# * formulario de propuesta de articulo


class ArticleProposalForm(forms.ModelForm):

    class Meta:
        model = ArticleProposal
        fields = [
            'title',
            'modality',
            'school',
            'new_school',
            'template',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2 ',
                    'placeholder': 'Título del artículo',
                    'required': 'true',
                    'data-validator': 'regex2title'
                }),
            'modality': forms.Select(attrs={'class': 'form-control mb-2 ', 'required': 'true'}),
            # 'placeholder': 'Escuela
            'school': forms.Select(attrs={
                'class': 'form-control mb-2 ',
            }
            ),
            'new_school': forms.TextInput(attrs={
                'class': 'form-control mb-2 ', 'placeholder': 'Nombre de la escuela',
                'disabled': 'true',
            }),
            'template': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-2 ',
                'accept': '.docx',
            })

        }

        help_texts = {
            'new_school': 'Si la escuela no se encuentra, seleccione "Otra" y escriba el nombre de la escuela en el campo de texto',
        }

        labels = {
            'title': 'Título',
            'modality': 'Modalidad',
            'school': 'Escuela',
            'new_school': '',
            'template': 'Plantilla',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # * concat queryset with option "Otra" with value "new"
        self.fields['school'].choices = [('', '---------')] + \
            [(school.id, school.name)
             for school in School.objects.all()] + [(None, 'Otra')]

        self.fields['new_school'].required = False

    def clean_template(self):
        template = self.cleaned_data['template']
        # * if not docx
        if template.name.split('.')[-1] != 'docx':
            raise forms.ValidationError(
                'El archivo no es un documento de Word')
        return template

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError(
                'El título no puede tener más de 100 caracteres')
        return title


class ArticleProposalUpdateForm(ArticleProposalForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # * if not school exclude school field
        self.fields['template'].required = False


class CoauthorForm(forms.ModelForm):

    class Meta:
        model = Coauthor
        fields = [
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'email',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'text-capitalize', 'placeholder': 'Nombre(s)',
                'required': 'true', 'pattern': 'regex2name',
            }),
            'apellido_paterno': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2 ',
                    'placeholder': 'Apellido paterno',
                    'required': 'true',
                    'pattern': 'regexalpha'
                }),
            'apellido_materno': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2 ',
                    'placeholder': 'Apellido materno',
                    'required': 'true',
                    'pattern': 'regexalpha'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control mb-2 ',
                    'placeholder': 'Correo electrónico',
                    'required': 'true',
                    'pattern': 'email'
                }),
        }

        labels = {
            'nombre': 'Nombre(s)',
            'apellido_paterno': 'Apellido paterno',
            'apellido_materno': 'Apellido materno',
            'email': 'Correo electrónico',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['nombre'].required = True
            self.fields['apellido_paterno'].required = True
            self.fields['apellido_materno'].required = True
            self.fields['email'].required = True


class ArticleImageForm(forms.ModelForm):

    class Meta:
        model = ArticleImage
        fields = [
            'image',
        ]

        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-2 ',
                'accept': '.jpg, .jpeg, .png',
                'required': 'true'
            }),
        }

        labels = {
            'image': 'Imagen',
        }
