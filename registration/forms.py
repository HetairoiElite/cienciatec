from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class UserCreationFromEmail(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text='Requerido. 254 caracteres como máximo y debe ser válido.')
    apellidoP = forms.CharField(
        required=True, help_text='Requerido. 30 caracteres como máximo.')
    apellidoM = forms.CharField(
        required=True, help_text='Requerido. 30 caracteres como máximo.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')  # * fields to show}

        # * fields from profile

    def __init__(self, *args, **kwargs):
        super(UserCreationFromEmail, self).__init__(*args, **kwargs)
        # Modificar en tiempo real los atributos del formulario
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario'})
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2 text-capitalize', 'placeholder': 'Nombres'})
        self.fields['apellidoP'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2 text-capitalize', 'placeholder': 'Apellido paterno'})
        self.fields['apellidoM'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2 text-capitalize', 'placeholder': 'Apellido materno'})
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Dirección de email'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Repite la contraseña'})

        # * no lables

        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        # * help text
        self.fields['first_name'].help_text = 'Requerido. 30 caracteres como máximo y solo letras.'
        self.fields['last_name'].help_text = 'Requerido. 150 caracteres como máximo y solo letras.'
        self.fields['password1'].help_text = '<ul><li>Tu contraseña no puede ser muy similar a tus otros datos personales.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser una contraseña común.</li><li>Tu contraseña no puede ser completamente numérica.</li></ul>'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'El email ya está registrado, prueba con otro.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        # * Max 2 names
        if len(first_name.split()) > 2:
            raise forms.ValidationError(
                'El nombre solo puede contener 2 nombres.')

        # * Only letters
        if len(first_name) > 30:
            raise forms.ValidationError(
                'El nombre debe contener máximo 30 caracteres.')

        if len(first_name) < 3:
            raise forms.ValidationError(
                'El nombre debe contener al menos 3 caracteres.')

        if len(first_name.split()) == 2:
            first_name = first_name.split()
            for name in first_name:
                if not name.isalpha():
                    raise forms.ValidationError(
                        'El nombre solo puede contener letras.')

            first_name = first_name[0].capitalize(
            ) + ' ' + first_name[1].capitalize()

        print(first_name)
        return first_name

    def clean_apellidoP(self):
        apellidoP = self.cleaned_data.get('apellidoP')
        if not apellidoP.isalpha():
            raise forms.ValidationError(
                'El apellido paterno solo puede contener letras.')

        if len(apellidoP) < 3:
            raise forms.ValidationError(
                'El apellido paterno debe contener al menos 3 caracteres.')

        if len(apellidoP) > 30:
            raise forms.ValidationError(
                'El apellido paterno debe contener máximo 30 caracteres.')
        return apellidoP.capitalize()

    def clean_apellidoM(self):
        apellidoM = self.cleaned_data.get('apellidoM')
        if not apellidoM.isalpha():
            raise forms.ValidationError(
                'El apellido materno solo puede contener letras.')

        if len(apellidoM) < 3:
            raise forms.ValidationError(
                'El apellido materno debe contener al menos 3 caracteres.')

        if len(apellidoM) > 30:
            raise forms.ValidationError(
                'El apellido materno debe contener máximo 30 caracteres.')
        return apellidoM.capitalize()

    def save(self, commit=True):
        user = super(UserCreationFromEmail, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['apellidoP'] + \
            ' ' + self.cleaned_data['apellidoM']
        user.is_active = False  # * send confirmation email
        if commit:
            user.save()
        return user


class UserCreationFormType(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('type_user',)

    def __init__(self, *args, **kwargs):
        super(UserCreationFormType, self).__init__(*args, **kwargs)
        self.fields['type_user'].widget.attrs.update(
            {'class': 'form-control mb-2'})

        self.fields['type_user'].label = ''

    def clean_type_user(self):
        type_user = self.cleaned_data.get('type_user')
        if type_user == '0':
            raise forms.ValidationError(
                'Debes seleccionar un tipo de usuario.')
        return type_user


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario o email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        self.fields['username'].label = ''
        self.fields['password'].label = ''

    def clean_username(self):
        email_or_username = self.cleaned_data.get('username')
        if User.objects.filter(email=email_or_username).exists():
            email_or_username = User.objects.get(
                email=email_or_username).username
            if not User.objects.get(username=email_or_username).is_active:
                raise forms.ValidationError(
                    'El usuario no está activo, revisa tu correo.')
        else:
            if not User.objects.filter(username=email_or_username).exists():
                raise forms.ValidationError(
                    'El usuario no existe.')

            else:
                if not User.objects.get(username=email_or_username).is_active:
                    raise forms.ValidationError(
                        'El usuario no está activo, revisa tu correo.')

        return email_or_username

    def clean_password(self):
        try:
            password = self.cleaned_data.get('password')
            user = User.objects.get(username=self.cleaned_data.get('username'))
            if not user.check_password(password):
                raise forms.ValidationError(
                    'La contraseña es incorrecta.')
        except User.DoesNotExist:
            pass
        return password


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'school']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file mt-3'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Modificar',
            'school': 'Escuela'
        }


class UserUpdateForm(forms.ModelForm):

    apellidoP = forms.CharField(max_length=30, required=True)
    apellidoM = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'apellidoP', 'apellidoM', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            # 'last_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2'}),
            'last_name': forms.HiddenInput(),
        }
        labels = {
            'first_name': 'Nombre/s'
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['apellidoP'].initial = self.instance.last_name.split(' ')[
            0]
        self.fields['apellidoM'].initial = self.instance.last_name.split(' ')[
            1]
        self.fields['apellidoP'].widget.attrs.update(
            {'class': 'form-control mb-2'})
        self.fields['apellidoM'].widget.attrs.update(
            {'class': 'form-control mb-2'})
        self.fields['apellidoP'].label = 'Apellido paterno'
        self.fields['apellidoM'].label = 'Apellido materno'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'El correo electrónico ya está en uso.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        # * Max 2 names
        if len(first_name.split()) > 2:
            raise forms.ValidationError(
                'El nombre solo puede contener 2 nombres.')

        # * Only letters
        if len(first_name) > 30:
            raise forms.ValidationError(
                'El nombre debe contener máximo 30 caracteres.')

        if len(first_name) < 3:
            raise forms.ValidationError(
                'El nombre debe contener al menos 3 caracteres.')

        if len(first_name.split()) == 2:
            first_name = first_name.split()
            for name in first_name:
                if not name.isalpha():
                    raise forms.ValidationError(
                        'El nombre solo puede contener letras.')

            first_name = first_name[0].capitalize(
            ) + ' ' + first_name[1].capitalize()

        print(first_name)
        return first_name

    def clean_apellidoP(self):
        apellidoP = self.cleaned_data.get('apellidoP')
        if len(apellidoP) > 30:
            raise forms.ValidationError(
                'El apellido paterno debe contener máximo 30 caracteres.')

        if len(apellidoP) < 3:
            raise forms.ValidationError(
                'El apellido paterno debe contener al menos 3 caracteres.')

        if not apellidoP.isalpha():
            raise forms.ValidationError(
                'El apellido paterno solo puede contener letras y no debe llevar espacios.')

        apellidoP = apellidoP.capitalize()

        return apellidoP

    def clean_apellidoM(self):
        apellidoM = self.cleaned_data.get('apellidoM')
        if len(apellidoM) > 30:
            raise forms.ValidationError(
                'El apellido materno debe contener máximo 30 caracteres.')

        if len(apellidoM) < 3:
            raise forms.ValidationError(
                'El apellido materno debe contener al menos 3 caracteres.')

        if not apellidoM.isalpha():
            raise forms.ValidationError(
                'El apellido materno solo puede contener letras y no debe llevar espacios.')

        apellidoM = apellidoM.capitalize()

        return apellidoM

    def clean_last_name(self):
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoM = self.cleaned_data.get('apellidoM')
        last_name = str(apellidoP) + ' ' + str(apellidoM)
        return last_name

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
