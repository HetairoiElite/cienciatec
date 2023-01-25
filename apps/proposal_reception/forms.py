
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
            'template',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['title'].label = 'Título'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Título del artículo'

        self.fields['modality'].required = True
        self.fields['modality'].label = 'Modalidad'
        self.fields['modality'].widget.attrs['class'] = 'form-control'

        self.fields['school'].required = True
        self.fields['school'].label = 'Escuela'
        self.fields['school'].widget.attrs['class'] = 'form-control'

        self.fields['template'].required = True
        self.fields['template'].label = 'Plantilla'
        self.fields['template'].widget.attrs['class'] = 'form-control'

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

        

class CoauthorForm(forms.ModelForm):

    class Meta:
        model = Coauthor
        fields = [
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['nombre'].label = 'Nombre(s)'
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre'

        self.fields['apellido_paterno'].required = True
        self.fields['apellido_paterno'].label = 'Apellido paterno'
        self.fields['apellido_paterno'].widget.attrs['class'] = 'form-control'
        self.fields['apellido_paterno'].widget.attrs['placeholder'] = 'Apellido paterno'

        self.fields['apellido_materno'].required = True
        self.fields['apellido_materno'].label = 'Apellido materno'
        self.fields['apellido_materno'].widget.attrs['class'] = 'form-control'
        self.fields['apellido_materno'].widget.attrs['placeholder'] = 'Apellido materno'

        self.fields['email'].required = True
        self.fields['email'].label = 'Correo electrónico'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo electrónico'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        # *max 2 names
        if len(nombre.split(' ')) > 2:
            raise forms.ValidationError(
                'El nombre no puede tener más de dos palabras')

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].label = 'Imagen'
        self.fields['image'].widget.attrs['class'] = 'form-control'
