
# * django

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

# * validate password
from django.contrib.auth import password_validation

# * views
from django.views.generic import View

from django.http import JsonResponse

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

# * locals

from .forms import *
from .models import Profile
from .tokens import account_activation_token


# Create your views here.
class SignUp(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    
    # * enviar email de confirmación de registro cuando el formulario es válido
    
    def form_valid(self, form):
        user = form.save()
        activateEmailSendLink(self.request, user, user.email)
        return super().form_valid(form)
    
    # * redireccionar al usuario a la página de inicio si ya está autenticado
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    # * success url
    
    def get_success_url(self):
        return reverse('registration:sent_email') + '?status=success'
    

# * UpdateProfile
@method_decorator(login_required, name='dispatch')
class UpdateProfile(FormView):
    template_name = 'registration/profile_form.html'
    form_class = ProfileUpdateForm
    
    # * pasar el usuario al form
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())
    
    # * si es la primera vez que se actualiza first_time = false
    # * si no es la primera vez redireccionar a la página de inicio
    
    def dispatch(self, request, *args, **kwargs):
        if 'edit' in request.GET:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('index')
    
    def get_success_url(self):
        # * agregar mensaje de éxito
        messages.add_message(self.request, messages.SUCCESS, 'Perfil actualizado correctamente')
        
        # * en la misma vista
        return reverse('registration:profile') + '?edit'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
    
def SentEmailView(request):
    if not request.GET.get('status'):
        return redirect('home')
    return render(request, 'registration/sent_email.html', {'status': request.GET.get('status')})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


def test_email(request):
    subject = 'Confirmación de registro'
    html_messsage = render_to_string(
        'registration/email_verification_msg.html', {'user': "kuan"})
    plaint_message = strip_tags(html_messsage)
    email_from = 'jonathan90090@gmail.com'
    recipient_list = ['jonathan90090@gmail.com']

    mail.send_mail(subject, plaint_message, email_from,
                   recipient_list, html_message=html_messsage)
    return redirect('login')


def activateEmailSendLink(request, user, to_email):
    mail_subject = 'Activación de cuenta.'
    message = render_to_string(
        'registration/email_verification_msg.html', {
            'user': user.first_name + " " + user.last_name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
    plaint_message = strip_tags(message)

    if send_mail(mail_subject, plaint_message, settings.EMAIL_HOST_USER, [to_email], html_message=message):
        return True
    else:
        return False


def reset_email_send_link(request, user, to_email):
    mail_subject = 'Cambio de contraseña.'
    message = render_to_string(
        'reset_password_mail.html', {
            'user': user.NombreCompleto(),
            'domain': "recover.applantar.com",
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https',
        })

    if send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email]):
        return True
    else:
        return False


def activeEmail(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not user.is_active and account_activation_token.check_if_token_expired(token):
            return render(request, 'registration/activate_email.html', {'status': 'warning', 'uidb64': uidb64, 'token': token})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_email.html', {'status': 'success'})
    else:
        return render(request, 'registration/activate_email.html', {'status': 'error'})


def new_link_active_email(request):
    try:
        uid = force_str(urlsafe_base64_decode(request.GET.get('uidb64')))
        user = User.objects.get(pk=uid)
        if not user.is_active:
            if activateEmailSendLink(request, user, user.email):
                context = {
                    'status': 'success',
                }
                return redirect(reverse('registration:sent_email')+f"?status={context['status']}")
            else:
                context = {
                    'status': 'error',
                }
                return redirect(reverse('sent_email')+f'?status={context["status"]}')
        else:
            context = {
                'status': 'warning',
            }
            return redirect(reverse('sent_email')+f'?status={context["status"]}')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {
        'status': 'error',
    }
    return redirect(reverse('sent_email')+f'?status={context["status"]}')


# * override de la vista de reset password

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Contraseña actualizada correctamente')
        return reverse('registration:profile')+ '?edit'
    
class ValidatePasswordView(View):

    def get(self, request, *args, **kwargs):
        # * password withouth user
        password = request.GET.get('password', None)

        try:
            validate = password_validation.validate_password(password)
            data = {
                'is_valid': True
            }
        except:
            data = {
                'is_valid': False
            }
        return JsonResponse(data)
