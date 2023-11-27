from apps.reviewer_assignment.models import Profile as RefeereProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# *authenticate

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from .models import Profile, TYPE_USER
from apps.school.models import School


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario o email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        self.fields['username'].label = 'Usuario o email'
        self.fields['password'].label = 'Contraseña'

    def clean_username(self):
        # * username or email
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                pass
        return username

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            user = authenticate(
                self.request, username=username, password=password
            )
            if user is None:
                raise forms.ValidationError("El usuario y la contraseña son incorrectos o puede ser que la cuenta aún no ha sido activada.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre de usuario',
        help_text='30 caracteres o menos. Solo letras, números y @/./+/-/_',
        widget=forms.TextInput(attrs={
            # 'pattern': 'regexusername',
            'placeholder': 'Nombre de usuario'
        }),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre(s)',
        help_text='30 caracteres o menos. Máximo 2 nombres.',
        widget=forms.TextInput(attrs={'pattern': 'regex2name',
                                      'placeholder': 'Nombre(s)'
                                      }),
    )
    apellidoP = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido paterno',
        widget=forms.TextInput(attrs={'pattern': 'regexalpha',
                                      'placeholder': 'Apellido paterno'
                                      }),
        help_text='30 caracteres o menos. Solo letras y espacios.',
    )
    apellidoM = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido materno',
        widget=forms.TextInput(attrs={'pattern': 'regexalpha',
                                      'placeholder': 'Apellido materno'
                                      }),
        help_text='30 caracteres o menos. Solo letras y espacios.',
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label='Correo electrónico',
        help_text='Se te enviará un correo electrónico para activar tu cuenta.',
        widget=forms.EmailInput(
            attrs={'pattern': 'email',
                   'placeholder': 'Correo electrónico'
                   })
    )
    password1 = forms.CharField(
        max_length=30,
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'data-validator': 'validpassword',
                   'placeholder': 'Contraseña'
                   }),
        help_text="""<li>Tu contraseña no puede ser muy similar a tus otros datos personales.</li>
            <li>Tu contraseña debe contener al menos 8 caracteres.</li>
            <li>Tu contraseña no puede ser una contraseña comúnmente usada.</li>
            <li>Tu contraseña no puede ser completamente numérica.</li>"""
    )
    password2 = forms.CharField(
        max_length=30,
        required=True,
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'data-equalto': 'id_password1',
                                          'placeholder': 'Confirmar contraseña'
                                          }),
        help_text='Introduce la misma contraseña.'
    )
    type_user = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=TYPE_USER,
        required=True,
        label='Tipo de usuario',
        help_text=f"""Si eres autor tendrás acceso a tu cuenta para empezar a hacer propuestas de articulos.
        
                      Si eres evaluador deberás esperar a que un administrador valide tu cuenta.""",
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'El nombre de usuario ya está en uso.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'El correo electrónico ya está en uso.')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        first_name = first_name.strip()
        first_name = first_name.capitalize()

        return first_name

    def clean_apellidoP(self):
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoP = apellidoP.strip()
        apellidoP = apellidoP.capitalize()

        return apellidoP

    def clean_apellidoM(self):
        apellidoM = self.cleaned_data.get('apellidoM')
        apellidoM = apellidoM.strip()
        apellidoM = apellidoM.capitalize()

        return apellidoM

    def save(self):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoM = self.cleaned_data.get('apellidoM')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        type_user = self.cleaned_data.get('type_user')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=apellidoP + ' ' + apellidoM,
            email=email,
            password=password,
            is_active=False
        )

        user.save()
        profile = Profile.objects.get(user=user)

        profile.type_user = type_user

        profile.save()

        return user


class ProfileUpdateForm(forms.Form):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(
        max_length=30,
        label='Nombre(s)',
        # * attrs
        widget=forms.TextInput(
            attrs={'pattern': 'regex2name',
                   'placeholder': 'Nombre(s)'
                   }),
        help_text='30 caracteres o menos. Máximo 2 nombres.'
    )
    apellidoP = forms.CharField(
        max_length=30,
        label='Apellido paterno',
        widget=forms.TextInput(
            attrs={'pattern': 'regexalpha',
                   'placeholder': 'Apellido paterno'
                   }),
        help_text='30 caracteres o menos.'
    )
    apellidoM = forms.CharField(
        max_length=30,
        label='Apellido materno',
        widget=forms.TextInput(
            attrs={'pattern': 'regexalpha',
                   'placeholder': 'Apellido materno'
                   }),
        help_text='30 caracteres o menos.'
    )
    # * many to many profiles
    profiles = forms.ModelMultipleChoiceField(
        label='Perfiles de arbitraje',
        queryset=RefeereProfile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Selecciona los perfiles para los que deseas arbitrar.'
    )

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        # * initial values

        self.fields['profiles'].initial = [
            profile.id for profile in user.profile.profiles.all()]

        # * get user from kwargs

        self.user = user

        profile = Profile.objects.get(user=user)
        self.fields['first_name'].initial = user.first_name
        try:
            self.fields['apellidoP'].initial = user.last_name.split()[0]
            self.fields['apellidoM'].initial = user.last_name.split()[1]
        except:
            pass

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        first_name = first_name.strip()
        first_name = first_name.capitalize()

        return first_name

    def clean_apellidoP(self):
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoP = apellidoP.strip()
        apellidoP = apellidoP.capitalize()

        return apellidoP

    def clean_apellidoM(self):
        apellidoM = self.cleaned_data.get('apellidoM')
        apellidoM = apellidoM.strip()
        apellidoM = apellidoM.capitalize()

        return apellidoM

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoM = self.cleaned_data.get('apellidoM')
        avatar = self.cleaned_data.get('avatar')

        user = self.user

        user.first_name = first_name
        user.last_name = apellidoP + ' ' + apellidoM

        user.save()

        profile = Profile.objects.get(user=user)

        if avatar != None:
            profile.avatar = avatar

        # * profiles
        profiles = self.cleaned_data.get('profiles')

        profile.profiles.clear()

        profile.profiles.set(profiles)

        profile.save()

        return user
