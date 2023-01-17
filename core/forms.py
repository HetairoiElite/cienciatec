from django import forms

from .models import Home

# * custom change form for home


class HomeChangeForm(forms.ModelForm):

    publication = forms.ModelChoiceField(
        queryset=Home.objects.first().publications.all().order_by('numero_publicacion'),
        empty_label='No hay publicaciones',
        widget=forms.RadioSelect(),
        required=True,
        help_text='Seleccione la publicación actual',
        label='Publicación actual'
    )

    def __init__(self, *args, **kwargs):
        super(HomeChangeForm, self).__init__(*args, **kwargs)
        self.fields['publication'].initial = Home.objects.first(
        ).publications.filter(current=True).first()

        # * remove label for image fields
        self.fields['image'].label = ''
        self.fields['brand_image'].label = ''
        self.fields['favicon'].label = ''
        self.fields['publication'].label = ''

        # * remove delete button for image fields

    class Meta:
        model = Home
        fields = '__all__'
        widgets = {
            'favicon': forms.FileInput(attrs={'accept': 'image/*'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'brand_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True):

        # * obtiene la publicación actual
        home = Home.objects.first()
        current_publication = home.publications.filter(current=True).first()

        # * si la publicación actual es diferente a la nueva publicación actual
        if current_publication != self.cleaned_data['publication']:
            # * actualiza la publicación actual
            current_publication.current = False
            current_publication.save()
            self.cleaned_data['publication'].current = True
            self.cleaned_data['publication'].save()

        return super(HomeChangeForm, self).save(commit)
