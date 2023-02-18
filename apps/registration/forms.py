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
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                try:
                    user = User.objects.get(
                        username=username, password=make_password(password))
                    if not user.is_active:
                        raise forms.ValidationError(
                            "Esta cuenta no está activa, revisa tu correo electrónico para activarla o contacta al administrador.")
                except User.DoesNotExist:
                    raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    apellidoP = forms.CharField(max_length=30, required=True)
    apellidoM = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput)
    type_user = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=TYPE_USER,
        required=True,
        label='Tipo de usuario',
        help_text=f"""Si eres autor tendrás acceso a tu cuenta para empezar a hacer propuestas de articulos.
        
                      Si eres evaluador deberás esperar a que un administrador valide tu cuenta.""",
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario'})

        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Nombre'})

        self.fields['apellidoP'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Apellido paterno'})
        self.fields['apellidoM'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Apellido materno'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Correo electrónico'})

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-2', 
             'placeholder': 'Confirmar contraseña',
             'aria-describedby':'example1Hint3',
             'aria-errormessage':'example1Error3',
             'data-equalto':'id_password1'
             })

        self.fields['type_user'].widget.attrs.update(
            {'class': 'form-check-input'})

        # * labels

        self.fields['username'].label = 'Nombre de usuario'
        self.fields['first_name'].label = 'Nombre(s)'
        self.fields['apellidoP'].label = 'Apellido paterno'
        self.fields['apellidoM'].label = 'Apellido materno'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['type_user'].label = 'Tipo de usuario'

        # * help text

        self.fields['username'].help_text = '30 caracteres o menos.'
        self.fields['first_name'].help_text = '30 caracteres o menos. Máximo 2 nombres.'
        self.fields['apellidoP'].help_text = '30 caracteres o menos.'
        self.fields['apellidoM'].help_text = '30 caracteres o menos.'
        self.fields['email'].help_text = 'Se te enviará un correo de confirmación.'
        self.fields['password1'].help_text = """
            <li>Tu contraseña no puede ser muy similar a tus otros datos personales.</li>
            <li>Tu contraseña debe contener al menos 8 caracteres.</li>
            <li>Tu contraseña no puede ser una contraseña comúnmente usada.</li>
            <li>Tu contraseña no puede ser completamente numérica.</li>
        """
        self.fields['password2'].help_text = 'Introduce la misma contraseña.'


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

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError(
                'La contraseña debe contener al menos 8 caracteres'
            )

        return password1

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                'Las contraseñas no coinciden'
            )

        return

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
    first_name = forms.CharField(max_length=30)
    apellidoP = forms.CharField(max_length=30)
    apellidoM = forms.CharField(max_length=30)
    # school = forms.ChoiceField(choices=[(0, 'Selecciona una escuela')])

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        # * choices for school

        # choices = [(0, 'Selecciona una escuela')]
        # choices.extend([(school.id, school.name)
        #                for school in School.objects.all()])

        # self.fields['school'].choices = choices

        # * labels
        self.fields['avatar'].label = 'Imagen de perfil'
        self.fields['first_name'].label = 'Nombre(s)'
        self.fields['apellidoP'].label = 'Apellido paterno'
        self.fields['apellidoM'].label = 'Apellido materno'
        # self.fields['school'].label = 'Escuela'

        # * attrs
        self.fields['avatar'].widget.attrs['class'] = 'help-text'
        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['apellidoP'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['apellidoM'].widget.attrs['class'] = 'form-control mb-2'
        # self.fields['school'].widget.attrs['class'] = 'form-control mb-2'

        # * placeholders
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nombre(s)'
        self.fields['apellidoP'].widget.attrs['placeholder'] = 'Apellido paterno'
        self.fields['apellidoM'].widget.attrs['placeholder'] = 'Apellido materno'

        self.fields['first_name'].help_text = '30 caracteres o menos. Máximo 2 nombres.'
        self.fields['apellidoP'].help_text = '30 caracteres o menos.'
        self.fields['apellidoM'].help_text = '30 caracteres o menos.'

        # * help text

        # self.fields['school'].help_text = 'Escuela a la que perteneces. Si no aparece tu escuela, contacta a un administrador para agregarla.'

        # * initial values

        # * get user from kwargs

        self.user = user

        profile = Profile.objects.get(user=user)
        self.fields['first_name'].initial = user.first_name
        try:
            self.fields['apellidoP'].initial = user.last_name.split()[0]
            self.fields['apellidoM'].initial = user.last_name.split()[1]
        except:
            pass

        # try:
        #     self.fields['school'].initial = profile.school.id
        # except:
        #     self.fields['school'].initial = 0
        # self.fields['avatar'].initial = profile.avatar

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

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        apellidoP = self.cleaned_data.get('apellidoP')
        apellidoM = self.cleaned_data.get('apellidoM')
        school = self.cleaned_data.get('school')
        avatar = self.cleaned_data.get('avatar')

        user = self.user

        user.first_name = first_name
        user.last_name = apellidoP + ' ' + apellidoM

        user.save()

        profile = Profile.objects.get(user=user)

        # try:
        #     # school = School.objects.get(id=school)
        #     profile.school = school
        # except:
        #     pass

        if avatar != None:
            profile.avatar = avatar

        profile.save()

        return user
