
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
            'title': forms.TextInput(attrs={'class': 'form-control mb-2 ', 'placeholder': 'Título del artículo', 'required': 'true'}),
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
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-2 ', 'placeholder': 'Nombre(s)', 'required': 'true'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control mb-2 ', 'placeholder': 'Apellido paterno', 'required': 'true'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control mb-2 ', 'placeholder': 'Apellido materno', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2 ', 'placeholder': 'Correo electrónico', 'required': 'true'}),
        }

        labels = {
            'nombre': 'Nombre(s)',
            'apellido_paterno': 'Apellido paterno',
            'apellido_materno': 'Apellido materno',
            'email': 'Correo electrónico',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        # *max 2 names
        if len(nombre.split(' ')) > 2:
            raise forms.ValidationError(
                'El nombre no puede tener más de dos nombres')

        # * if 2 names check if they are valid
        if len(nombre.split(' ')) == 2:
            if not nombre.split(' ')[0].isalpha() or not nombre.split(' ')[1].isalpha():
                raise forms.ValidationError(
                    'El nombre solo puede contener letras')

        # * if 1 name check if it is valid
        if len(nombre.split(' ')) == 1:
            if not nombre.isalpha():
                raise forms.ValidationError(
                    'El nombre solo puede contener letras')

        return nombre

    def clean_apellido_paterno(self):
        apellido_paterno = self.cleaned_data['apellido_paterno']
        if not apellido_paterno.isalpha():
            raise forms.ValidationError(
                'El apellido paterno solo puede contener letras')
        return apellido_paterno

    def clean_apellido_materno(self):
        apellido_materno = self.cleaned_data['apellido_materno']
        if not apellido_materno.isalpha():
            raise forms.ValidationError(
                'El apellido materno solo puede contener letras')
        return apellido_materno


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
            }),
        }

        labels = {
            'image': 'Imagen',
        }
